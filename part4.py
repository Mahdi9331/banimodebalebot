import time
import requests
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BALE_TOKEN = "660809460:U8jqeU20ph9Cc8eFGLZYImGJIntcI1dHZJc"
CHAT_ID = "2087326516"

# 🟢 لینک‌های بخش ۴
TARGETS = [
    {"name": "برند هالیدی", "url": "https://www.banimode.com/Brand/693/%D9%87%D8%A7%D9%84%DB%8C%D8%AF%DB%8C?category=832%2C871%2C1338%2C11%2C1630%2C8%2C703%2C3205%2C1545%2C1544%2C3&sort%7Cprice=asc"},
    {"name": "کاپشن مردانه", "url": "https://www.banimode.com/883/%DA%A9%D8%A7%D9%BE%D8%B4%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کفش روزمره", "url": "https://www.banimode.com/815/%DA%A9%D9%81%D8%B4-%D8%B1%D9%88%D8%B2%D9%85%D8%B1%D9%87-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"}
]

def take_optimized_screenshot(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.set_page_load_timeout(50)
        try: driver.get(url)
        except: pass
        time.sleep(4)
        
        height_needed = 1200 
        driver.execute_script(f"window.scrollTo(0, {height_needed});")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        driver.set_window_size(1280, height_needed + 200)
        driver.save_screenshot("shot.png")
        return "shot.png"
    except:
        return None
    finally:
        driver.quit()

def send_photo(image, caption):
    url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto"
    for i in range(3):
        try:
            with open(image, "rb") as f:
                requests.post(url, files={"photo": f}, data={"chat_id": CHAT_ID, "caption": caption}, timeout=40)
            return True
        except:
            time.sleep(2)
    return False

def check_command():
    try:
        res = requests.get(f"https://tapi.bale.ai/bot{BALE_TOKEN}/getUpdates", timeout=10).json()
        if not res.get('result'): return False
        msg = res['result'][-1]['message']
        if str(msg['chat']['id']) == CHAT_ID and int(time.time()) - msg['date'] < 1200:
            text = msg.get('text', '')
            if "لیست" in text or "list" in text.lower():
                # فقط در پارت آخر پیام پایان بفرست
                requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "✅ تمام لینک‌ها بررسی شد."})
                return True
    except: pass
    return False

if __name__ == "__main__":
    if check_command():
        print("✅ پارت ۴ شروع شد...")
        for item in TARGETS:
            img = take_optimized_screenshot(item['url'])
            if img:
                if not send_photo(img, f"🛍 {item['name']}\n🔗 {item['url']}"):
                    requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": f"❌ عکس نیامد: {item['name']}\n{item['url']}"})
                try: os.remove(img)
                except: pass
            else:
                requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": f"⚠️ خطا در عکس: {item['name']}\n{item['url']}"})
            time.sleep(2)
