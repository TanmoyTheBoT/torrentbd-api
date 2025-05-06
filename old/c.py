import requests

# Step 1: Get token from local solver API
url = "http://127.0.0.1:8000/solve_recaptcha/"
params = {
    "site_key": "6LcR_okUAAAAAPYrPe-HK_0RULO1aZM15ENyM-Mf",  # site key for the recaptcha
    "page_url": "https://antcpt.com/score_detector/"  # URL where the recaptcha is
}
headers = {
    "accept": "application/json"
}

response = requests.post(url, params=params, headers=headers)
RECAPTCHA_TOKEN = response.json().get("gRecaptchaResponse")
print("RECAPTCHA_TOKEN:", RECAPTCHA_TOKEN)

# Step 2: Verify the token using AntCPT API
antcpt_url = "https://antcpt.com/score_detector/verify.php"
verify_headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9,bn;q=0.8",
    "content-type": "application/json",
    "origin": "https://antcpt.com",
    "priority": "u=1, i",
    "referer": "https://antcpt.com/score_detector/",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
verify_data = {
    "g-recaptcha-response": RECAPTCHA_TOKEN
}

verify_response = requests.post(antcpt_url, headers=verify_headers, json=verify_data)
verify_result = verify_response.json()

# Print the verification result and score
print("Verification Result:", verify_result)
print("Score:", verify_result.get("score"))
