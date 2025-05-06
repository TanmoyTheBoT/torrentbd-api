import requests
import http.cookiejar as cookiejar

# Load cookies from a Netscape-style cookies.txt file
cookies = cookiejar.MozillaCookieJar("cookies.txt")
cookies.load(ignore_discard=True, ignore_expires=True)

# Attach cookies to a session
session = requests.Session()
session.cookies = cookies

# Define headers similar to the actual AJAX request
headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.torrentbd.net",
    "Referer": "https://www.torrentbd.net/",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# Define the form data (search parameters)
data = {
    "page": 1,
    "kuddus_searchtype": "torrents",
    "kuddus_searchkey": "hello",
    "searchParams[sortBy]": "",
    "searchParams[secondary_filters_extended]": ""
}

# Send the POST request to the AJAX search endpoint
search_url = "https://www.torrentbd.net/ajsearch.php"
response = session.post(search_url, headers=headers, data=data)

# Output response
print("🔍 Search Request Status Code:", response.status_code)
print("📄 Response Text Preview:\n")
print(response.text[:2000])  # preview first 2000 characters

# Save to file for easier review
with open("search_response.html", "w", encoding="utf-8") as f:
    f.write(response.text)
