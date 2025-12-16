import time
import requests
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BALE_TOKEN = "660809460:U8jqeU20ph9Cc8eFGLZYImGJIntcI1dHZJc"
CHAT_ID = "2087326516"

# 🟢 لینک‌های بخش ۱
TARGETS = [
    {"name": "کت تک مردانه", "url": "https://www.banimode.com/1319/%DA%A9%D8%AA-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "پیراهن مردانه (همه)", "url": "https://www.banimode.com/11/%D9%BE%DB%8C%D8%B1%D8%A7%D9%87%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "پیراهن مردانه (برندها)", "url": "https://www.banimode.com/11/%D9%BE%DB%8C%D8%B1%D8%A7%D9%87%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?brand=694%2C2113%2C3274%2C522%2C4%2C469%2C1552%2C479%2C1414%2C3328%2C631%2C1238%2C1293%2C1018%2C1256%2C2455%2C693%2C665%2C2038%2C360%2C1%2C2%2C683%2C614%2C415%2C1040%2C849%2C1276%2C3427%2C1335%2C377%2C2080%2C3151%2C445%2C965%2C801%2C82%2C2524%2C1072%2C2713%2C905%2C748%2C488%2C921%2C823%2C733%2C848%2C1148%2C3730&sort%7Cprice=asc"},
    {"name": "ژاکت و پلیور", "url": "https://www.banimode.com/9/%DA%98%D8%A7%DA%A9%D8%AA-%D9%88-%D9%BE%D9%84%DB%8C%D9%88%D8%B1-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "شلوار کتان", "url": "https://www.banimode.com/371/%D8%B4%D9%84%D9%88%D8%A7%D8%B1-%DA%A9%D8%AA%D8%A7%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"}
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
        
        # اسکرول تا حدود ۸ محصول اول
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
                return True
    except: pass
    return False

if __name__ == "__main__":
    if check_command():
        print("✅ پارت ۱ شروع شد...")
        # فقط در پارت اول دکمه ارسال می‌شود تا کاربر بداند شروع شده
        requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "✅ دستور دریافت شد. شروع ارسال عکس‌ها..."})
        
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
