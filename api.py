import requests
import pyotp
import json
from dotenv import load_dotenv
import os
import http.cookiejar as cookielib

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

if os.path.exists(cookies_file):
    print("🍪 Loading cookies from file...")
    cookiejar = cookielib.MozillaCookieJar(cookies_file)
    cookiejar.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cookiejar  # 🔧 Assign directly to session

    # Check if still logged in
    verify_url = "https://www.torrentbd.net/"
    verify_response = session.get(verify_url, headers=headers)
    with open("responsetest.html", "w", encoding="utf-8") as f:
        f.write(verify_response.text)

    if "home - torrentbd" in verify_response.text.lower():
        print("✅ Cookies are valid. Already logged in.")
        logged_in = True
    else:
        print("⚠️ Cookies are invalid or expired. Need to login.")

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
        "login_phase": "1",
        "_remember": "yes",
        "extra": ""
    }

    response = session.post(login_url, data=payload)

    # Debug info
    print("\n📨 Raw Response Headers:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")

    print("\n🧾 Raw Response Body:")
    print(response.text[:1000])  # Limit output

    if "login successful" in response.text.lower():
        print("✅ Login successful!")

        # Save cookies in Netscape format
        cookiejar = cookielib.MozillaCookieJar(cookies_file)
        for cookie in session.cookies:
            cookiejar.set_cookie(cookie)
        cookiejar.save(ignore_discard=True, ignore_expires=True)

        print("🍪 Cookies saved to cookies.txt")

        print("\n🔍 Saved Cookies:")
        for cookie in session.cookies:
            print(f"{cookie.domain}\t{cookie.path}\t{cookie.name}\t{cookie.value}")
    else:
        print("❌ Login failed.")
