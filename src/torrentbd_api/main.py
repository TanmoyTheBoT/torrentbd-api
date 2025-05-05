from torrentbd_api.login import login, check_login_status
from torrentbd_api.api import app
import uvicorn



def ensure_login():
    if not check_login_status():
        login()


def main():
    ensure_login()
    uvicorn.run("torrentbd_api.api:app", host="0.0.0.0", port=5000, reload=True)



if __name__ == "__main__":
    main()