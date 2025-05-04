from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import uvicorn
app = FastAPI()

def get_recaptcha_token(site_key: str, page_url: str):
    chrome_options = Options()
    # Uncomment this to run in headless mode
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(page_url)
        time.sleep(3)  # Let the page and scripts load

        # Wait for grecaptcha to be available
        for i in range(10):
            has_grecaptcha = driver.execute_script("return typeof grecaptcha !== 'undefined' && typeof grecaptcha.execute === 'function';")
            if has_grecaptcha:
                break
            time.sleep(1)
        else:
            raise Exception("grecaptcha not loaded on the page")

        # Execute grecaptcha and wait for token
        token = driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            grecaptcha.execute(arguments[0], { action: 'auth_login' }).then(function(token) {
                callback(token);
            }).catch(function(error) {
                callback("ERROR: " + error.message);
            });
        """, site_key)

        if token.startswith("ERROR:"):
            raise Exception(token)

        return token

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"reCAPTCHA error: {str(e)}")
    finally:
        driver.quit()

@app.post("/solve_recaptcha/")
async def solve_recaptcha(site_key: str, page_url: str):
    token = get_recaptcha_token(site_key, page_url)
    return {"gRecaptchaResponse": token}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)