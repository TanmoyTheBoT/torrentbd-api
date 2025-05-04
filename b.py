import requests
import http.cookiejar as cookiejar

# Load cookies from a Netscape-style cookies.txt file
cookies = cookiejar.MozillaCookieJar("cookies.txt")
cookies.load(ignore_discard=True, ignore_expires=True)

# Attach cookies to a session
session = requests.Session()
session.cookies = cookies

# Set headers to mimic a real browser
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,bn;q=0.8",
    "cache-control": "max-age=0",
    "referer": "https://www.torrentbd.net",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": "135.0.7049.116",
    "sec-ch-ua-full-version-list": '"Google Chrome";v="135.0.7049.116", "Not-A.Brand";v="8.0.0.0", "Chromium";v="135.0.7049.116"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": "19.0.0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# Request the page using session with loaded cookies
url = "https://www.torrentbd.net/"
response = session.get(url, headers=headers)

# Output response
print("📥 Status Code:", response.status_code)
print("📄 Raw HTML Preview:\n")
print(response.text)  # Just preview first 2000 characters
with open("response.html", "w", encoding="utf-8") as f:
    f.write(response.text)  # Save first 2000 characters to file for preview
