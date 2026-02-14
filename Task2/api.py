import asyncio
import uuid
import json
import random
import math
import os
import numpy as np
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

app = FastAPI()
TASKS = {}

class RecaptchaRequest(BaseModel):
    proxy: str = None

def get_human_curve(start, end):
    points = [start, 
              (start[0] + random.randint(-50, 50), start[1] + random.randint(-50, 50)),
              (end[0] + random.randint(-10, 10), end[1] + random.randint(-10, 10)),
              end]
    n = len(points)
    steps = random.randint(35, 55)
    t_values = np.linspace(0, 1, steps)
    curve = []
    for t in t_values:
        x = sum(math.comb(n-1, i) * (1-t)**(n-1-i) * t**i * points[i][0] for i in range(n))
        y = sum(math.comb(n-1, i) * (1-t)**(n-1-i) * t**i * points[i][1] for i in range(n))
        curve.append((x, y))
    return curve

async def solve_mechanism(task_id: str, proxy_str: str = None):
    TASKS[task_id] = {"status": "processing", "token_value": None}
    
    async with Stealth().use_async(async_playwright()) as p:
        try:
            session_dir = os.path.abspath(f"proxy_sessions/task_{task_id}")
            launch_args = {
                "user_data_dir": session_dir,
                "headless": False, 
                "args": ["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            }

            if proxy_str:
                auth, server = proxy_str.split('@')
                user, pwd = auth.split(':')
                launch_args["proxy"] = {"server": f"http://{server}", "username": user, "password": pwd}

            context = await p.chromium.launch_persistent_context(**launch_args)
            page = context.pages[0]

            # --- TOKEN INTERCEPTION ---
            async def handle_response(response):
                if "google.com/recaptcha/api2/reload" in response.url:
                    try:
                        text = await response.text()
                        if '["rresp","' in text:
                            token = text.split('["rresp","')[1].split('"')[0]
                            TASKS[task_id]["token_value"] = token
                    except: pass
            
            page.on("response", handle_response)

            # 1. Navigate and wait for Network Idle
            # This ensures all scripts (including Google's) are downloaded
            await page.goto("https://cd.captchaaiplus.com/recaptcha-v3-2.php", wait_until="networkidle")

            # 2. Hard Verification: Wait for grecaptcha object and execute function
            # This solves the "execute is not a function" error
            await page.wait_for_function(
                "() => typeof grecaptcha !== 'undefined' && typeof grecaptcha.execute === 'function'",
                timeout=20000
            )

            # 3. Human interaction
            await page.mouse.wheel(0, random.randint(200, 400))
            btn = page.locator("#btn")
            box = await btn.bounding_box()
            target_pos = (box['x'] + box['width']/2, box['y'] + box['height']/2)
            
            path = get_human_curve((0,0), target_pos)
            for x, y in path:
                await page.mouse.move(x, y)
            
            await btn.click()

            # 4. Wait for score extraction
            await page.wait_for_function(
                '() => document.getElementById("out").innerText.includes("score")', 
                timeout=15000
            )
            
            raw_output = await page.inner_text("#out")
            data = json.loads(raw_output)
            google_res = data.get("google_response", {})
            
            TASKS[task_id].update({
                "status": "completed",
                "score": google_res.get("score"),
                "success_text": google_res.get("action"),
                "verification_date": google_res.get("challenge_ts")
            })

            await context.close()
        except Exception as e:
            TASKS[task_id] = {"status": "failed", "error": str(e)}

@app.post("/recaptcha/in")
async def create_task(request: RecaptchaRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(solve_mechanism, task_id, request.proxy)
    return {"TaskID": task_id}

@app.get("/recaptcha/res")
async def get_result(task_id: str):
    return TASKS.get(task_id, {"status": "not_found"})

if __name__ == "__main__":
    import uvicorn
    if not os.path.exists("proxy_sessions"): os.makedirs("proxy_sessions")
    uvicorn.run(app, host="127.0.0.1", port=8000)