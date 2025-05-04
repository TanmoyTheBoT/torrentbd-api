import requests

url = "http://127.0.0.1:8000/solve_recaptcha/"
params = {
    "site_key": "6Lci27UZAAAAAPMvFNNodcgJhYyB8D3MrnaowTqe",
    "page_url": "https://www.torrentbd.net/"
}
headers = {
    "accept": "application/json"
}
response = requests.post(url, params=params, headers=headers)
RECAPTCHA_TOKEN = response.json().get("gRecaptchaResponse")
print("RECAPTCHA_TOKEN:", RECAPTCHA_TOKEN)
