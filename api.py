import requests
import pyotp
import json
from dotenv import load_dotenv
import os
import http.cookiejar as cookiejar

load_dotenv()

# === Step 1: Get reCAPTCHA token from FastAPI ===
print("🔄 Requesting reCAPTCHA token...")

url = "http://127.0.0.1:8000/solve_recaptcha/"
params = {
    "site_key": "6Lci27UZAAAAAPMvFNNodcgJhYyB8D3MrnaowTqe",
    "page_url": "https://www.torrentbd.net/"
}
headers = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

try:
    response = requests.post(url, params=params, headers=headers)
    response.raise_for_status()
    RECAPTCHA_TOKEN = response.json().get("gRecaptchaResponse")
    if not RECAPTCHA_TOKEN:
        raise ValueError("No token returned")
    print("✅ reCAPTCHA token received")
except Exception as e:
    print(f"❌ Failed to get reCAPTCHA token: {e}")
    exit(1)

# === Step 2: Prepare session and check cookies ===
session = requests.Session()
cookies_file = "cookies.txt"
logged_in = False

def is_cookie_file_valid(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return len(content) > 0
    except Exception:
        return False

if os.path.exists(cookies_file) and is_cookie_file_valid(cookies_file):
    print("🍪 Loading cookies from file...")
    cookiejar = cookiejar.MozillaCookieJar(cookies_file)
    try:
        cookiejar.load(ignore_discard=True, ignore_expires=True)
        session.cookies = cookiejar
    except Exception as e:
        print(f"⚠️ Failed to load cookies properly: {e}")
    else:
        # Check login status
        verify_url = "https://www.torrentbd.net/"
        try:
            verify_response = session.get(verify_url, headers=headers)

            if "home - torrentbd" in verify_response.text.lower():
                print("✅ Cookies are valid. Already logged in.")
                logged_in = True
            else:
                print("⚠️ Cookies loaded but user seems not logged in.")
        except Exception as e:
            print(f"❌ Failed to verify login with cookies: {e}")
else:
    print("📂 Cookie file missing or blank.")

# === Step 3: Login if not already ===
if not logged_in:
    print("🔐 Attempting login...")

    otp = pyotp.TOTP(os.getenv('TOTP_SECRET')).now()
    print(f"Generated OTP: {otp}")

    login_url = "https://www.torrentbd.net/ajtakelogin.php"

    payload = {
        "username": os.getenv('USERNAME'),
        "password": os.getenv('PASSWORD'),
        "auth_login": "",
        "recaptcha_token": RECAPTCHA_TOKEN,
        "otp": otp,
        "login_phase": "2",
        "_remember": "yes",
        "extra": ""
    }

    try:
        response = session.post(login_url, data=payload, headers=headers)
        if "login successful" in response.text.lower():
            print("✅ Login successful!")
            # Save browser-style cookies
            cookiejar = cookiejar.MozillaCookieJar(cookies_file)
            for cookie in session.cookies:
                cookiejar.set_cookie(cookie)
            cookiejar.save(ignore_discard=True, ignore_expires=True)
            print("🍪 cookies saved to cookies.txt")

        else:
            print("❌ Login failed. Check credentials or CAPTCHA.")
    except Exception as e:
        print(f"❌ Login request failed: {e}")
