import asyncio
import json
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

URL = "https://egypt.blsspainglobal.com/Global/CaptchaPublic/GenerateCaptcha?data=4CDiA9odF2%2b%2bsWCkAU8htqZkgDyUa5SR6waINtJfg1ThGb6rPIIpxNjefP9UkAaSp%2fGsNNuJJi5Zt1nbVACkDRusgqfb418%2bScFkcoa1F0I%3d"

async def scrape_task_3():
    # Keeping your preferred Stealth initialization method
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        print("Opening URL...")
        await page.goto(URL, wait_until="networkidle")
        await asyncio.sleep(5) 

        # --- Human Visibility Filter ---
        async def is_human_visible(target_page, element):
            return await target_page.evaluate('''
                (el) => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    if (parseFloat(style.opacity) < 0.1 || style.display === 'none' || style.visibility === 'hidden') return false;
                    
                    const x = rect.left + rect.width / 2;
                    const y = rect.top + rect.height / 2;
                    const topEl = document.elementFromPoint(x, y);
                    
                    return el.contains(topEl) || topEl.contains(el);
                }
            ''', element)

        all_images_data = []
        visible_images_data = []

        # 1 & 2. Scrape images from Main Page AND any Iframes
        for frame in page.frames:
            img_elements = await frame.query_selector_all("img")
            
            for img in img_elements:
                src = await img.get_attribute("src")
                if not src: continue
                
                all_images_data.append(src)
                
                # Check visibility and dimensions for the grid
                if await is_human_visible(frame, img):
                    box = await img.bounding_box()
                    if box:
                        # Logic: Captcha tiles are squares (aspect ratio ~1.0) 
                        # and usually between 50px and 150px wide.
                        aspect_ratio = box['width'] / box['height']
                        is_square = 0.85 <= aspect_ratio <= 1.15
                        is_tile_size = 40 < box['width'] < 200
                        
                        if is_square and is_tile_size:
                            visible_images_data.append(src)

        # Ensure we only keep the 9 grid images (filters out square social icons if any)
        # Typically the captcha images load sequentially in the DOM.
        visible_images_data = visible_images_data[:9]

        # Save results
        with open("allimages.json", "w") as f:
            json.dump(all_images_data, f, indent=4)

        with open("visible_images_only.json", "w") as f:
            json.dump(visible_images_data, f, indent=4)

        # 3. Scrape ONLY the single visible instruction
        all_instructions = await page.query_selector_all(".captcha-instruction, .box-label, p, span, b")
        visible_instruction = "Not Found"
        for inst in all_instructions:
            text = await inst.inner_text()
            if any(k in text.lower() for k in ["select", "click", "match"]):
                if await is_human_visible(page, inst):
                    visible_instruction = text.strip()
                    break

        print("\n" + "="*50)
        print("TASK 3 FINAL SUMMARY")
        print("="*50)
        print(f"Instruction: {visible_instruction}")
        print(f"Total Images Scraped: {len(all_images_data)}")
        print(f"Visible Grid Images: {len(visible_images_data)} (Target: 9)")
        print("-" * 50)
        print("Files Saved: allimages.json, visible_images_only.json")
        print("="*50)

        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(scrape_task_3())