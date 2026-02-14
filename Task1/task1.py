import asyncio
import random
import math
import json
import numpy as np
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# --- CONFIGURATION ---
TOTAL_TESTS = 250
TESTS_PER_IP = 12 
MAX_CONCURRENT_SESSIONS = 5 
OUTPUT_FILE = "results.jsonl"
FILE_LOCK = asyncio.Lock()
USE_LOCAL_LAN_EVERY = 4 

RAW_PROXIES = [
    "ivcoakag:cii4n2vq1nyx@192.46.187.22:6600",
    "ivcoakag:cii4n2vq1nyx@82.23.62.152:7905",
    "ivcoakag:cii4n2vq1nyx@130.180.236.143:6148",
    "ivcoakag:cii4n2vq1nyx@104.253.109.226:5504",
    "ivcoakag:cii4n2vq1nyx@46.203.30.234:6235",
    "ivcoakag:cii4n2vq1nyx@82.21.42.244:7506",
    "ivcoakag:cii4n2vq1nyx@82.23.61.60:7812",
    "ivcoakag:cii4n2vq1nyx@46.203.60.16:7016",
    "ivcoakag:cii4n2vq1nyx@46.203.60.208:7208",
    "ivcoakag:cii4n2vq1nyx@82.22.181.228:7939"
]

def parse_proxy(proxy_str):
    auth, server = proxy_str.split('@')
    user, pwd = auth.split(':')
    return {"server": f"http://{server}", "username": user, "password": pwd, "ip": server.split(':')[0]}

async def save_result(data):
    async with FILE_LOCK:
        with open(OUTPUT_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")

def get_human_curve(start, end):
    points = [start, 
              (start[0] + random.randint(-60, 60), start[1] + random.randint(-60, 60)),
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

async def run_single_iteration(page, iteration, proxy_ip, last_pos):
    try:
        # Step 1: Human Warmup on Google
        await page.goto("https://www.google.com", wait_until="commit")
        await asyncio.sleep(random.uniform(1.0, 2.0))

        # Step 2: Navigate to target site
        await page.goto("https://cd.captchaaiplus.com/recaptcha-v3-2.php", wait_until="domcontentloaded")
        
        # --- FIX FOR "grecaptcha.execute is not a function" ---
        # Wait until the grecaptcha object exists and has the execute method
        print(f"[{iteration}] Waiting for reCAPTCHA API to load...")
        try:
            await page.wait_for_function(
                "() => typeof grecaptcha !== 'undefined' && typeof grecaptcha.execute === 'function'", 
                timeout=15000
            )
        except Exception:
            print(f"[{iteration}] reCAPTCHA API failed to load (Timeout).")
            return last_pos, 0.1
        # -----------------------------------------------------

        await page.mouse.wheel(0, random.randint(200, 500))
        await asyncio.sleep(random.uniform(0.5, 1.0))

        btn = page.locator("#btn")
        box = await btn.bounding_box()
        if not box: return last_pos, 0.1
        
        target = (box['x'] + box['width']/2, box['y'] + box['height']/2)
        path = get_human_curve(last_pos, target)
        for x, y in path:
            await page.mouse.move(x, y)
        
        # Small delay before clicking mimics human preparation
        await asyncio.sleep(random.uniform(0.2, 0.5))
        await btn.click()

        # Wait for the output JSON to appear in the 'out' element
        await page.wait_for_function(
            '() => document.getElementById("out").innerText.includes("score")', 
            timeout=15000
        )
        
        output_text = await page.inner_text("#out")
        output = json.loads(output_text)
        res = output.get("google_response", {})
        score = res.get("score", 0.1)
        
        await save_result({
            "iteration": iteration, 
            "ip": proxy_ip, 
            "score": score, 
            "ts": res.get("challenge_ts"),
            "action": res.get("action")
        })
        
        print(f"[{iteration}] IP: {proxy_ip} | Score: {score}")
        return target, score

    except Exception as e:
        print(f"[{iteration}] Error: {str(e)[:70]}")
        return (0, 0), 0.1

async def manage_session(p, proxy_str, session_idx, session_id_start, semaphore):
    async with semaphore:
        use_lan = (session_idx % USE_LOCAL_LAN_EVERY == 0)
        
        if use_lan:
            p_info = {"server": None, "ip": f"LAN_Node_{session_idx}"}
            session_dir = os.path.abspath(f"proxy_sessions/lan_node_{session_idx}")
        else:
            p_info = parse_proxy(proxy_str)
            session_dir = os.path.abspath(f"proxy_sessions/proxy_{p_info['ip']}")

        launch_args = {
            "user_data_dir": session_dir,
            "headless": False,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ],
            "viewport": {'width': 1280, 'height': 720},
        }
        
        if p_info["server"]:
            launch_args["proxy"] = {
                "server": p_info["server"],
                "username": p_info["username"],
                "password": p_info["password"]
            }

        try:
            # Persistent context using the stealth-wrapped 'p'
            context = await p.chromium.launch_persistent_context(**launch_args)
            page = context.pages[0]
            
            mouse_pos = (random.randint(0, 100), random.randint(0, 100))

            for s_iter in range(TESTS_PER_IP):
                current_total = session_id_start + s_iter
                if current_total >= TOTAL_TESTS: break
                
                mouse_pos, score = await run_single_iteration(page, current_total + 1, p_info['ip'], mouse_pos)
                
                # Dynamic cooldown: Local LAN and High scores can move faster
                base_wait = 12 if score >= 0.7 else 30
                await asyncio.sleep(random.uniform(base_wait, base_wait + 10))

            await context.close()
        except Exception as e:
            print(f"Session Crash [{p_info['ip']}]: {e}")

async def main():
    if not os.path.exists("proxy_sessions"): os.makedirs("proxy_sessions")
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_SESSIONS)
    
    # Recommended Stealth Usage
    async with Stealth().use_async(async_playwright()) as p:
        tasks = []
        for idx, i in enumerate(range(0, TOTAL_TESTS, TESTS_PER_IP)):
            # Rotate through the proxy list
            proxy_str = RAW_PROXIES[(i // TESTS_PER_IP) % len(RAW_PROXIES)]
            tasks.append(manage_session(p, proxy_str, idx, i, semaphore))
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())