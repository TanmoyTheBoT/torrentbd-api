import requests
import pyotp
import json
from dotenv import load_dotenv
import os
import http.cookiejar as cj
from v3cap.captcha import get_recaptcha_token as fetch_recaptcha_token

load_dotenv()

session = requests.Session()
cookies_file = "cookies.txt"
headers = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}


def get_recaptcha_token():
    print("🔄 Requesting reCAPTCHA token...")
    try:
        token = fetch_recaptcha_token(
            site_key="6Lci27UZAAAAAPMvFNNodcgJhYyB8D3MrnaowTqe",
            page_url="https://www.torrentbd.net"
        )
        if not token:
            raise ValueError("No token returned")
        print("✅ reCAPTCHA token received")
        return token
    except Exception as e:
        print(f"❌ Failed to get reCAPTCHA token: {e}")
        exit(1)


def is_cookie_file_valid(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return len(f.read().strip()) > 0
    except:
        return False


def check_login_status():
    logged_in = False
    if os.path.exists(cookies_file) and is_cookie_file_valid(cookies_file):
        print("🍪 Loading cookies from file...")
        cookiejar = cj.MozillaCookieJar(cookies_file)
        try:
            cookiejar.load(ignore_discard=True, ignore_expires=True)
            session.cookies = cookiejar
        except Exception as e:
            print(f"⚠️ Failed to load cookies properly: {e}")
        else:
            try:
                resp = session.get("https://www.torrentbd.net/", headers=headers)
                if "home - torrentbd" in resp.text.lower():
                    print("✅ Cookies are valid. Already logged in.")
                    logged_in = True
                else:
                    print("⚠️ Cookies loaded but user seems not logged in.")
            except Exception as e:
                print(f"❌ Failed to verify login: {e}")
    else:
        print("📂 No valid cookie file.")
    return logged_in


def login():
    token = get_recaptcha_token()
    otp = pyotp.TOTP(os.getenv('TOTP_SECRET')).now()
    print(f"🔐 Generated OTP: {otp}")

    payload = {
        "username": os.getenv('USERNAME'),
        "password": os.getenv('PASSWORD'),
        "auth_login": "",
        "recaptcha_token": token,
        "otp": otp,
        "login_phase": "2",
        "_remember": "yes",
        "extra": ""
    }

    try:
        response = session.post("https://www.torrentbd.net/ajtakelogin.php", data=payload, headers=headers)
        if "login successful" in response.text.lower():
            print("✅ Login successful!")
            cookiejar_obj = cj.MozillaCookieJar(cookies_file)
            for c in session.cookies:
                cookiejar_obj.set_cookie(c)
            cookiejar_obj.save(ignore_discard=True, ignore_expires=True)
            print("🍪 Cookies saved to cookies.txt")
        else:
            print("❌ Login failed. Check credentials or CAPTCHA.")
    except Exception as e:
        print(f"❌ Login request failed: {e}")


if __name__ == "__main__":
    if not check_login_status():
        login()
