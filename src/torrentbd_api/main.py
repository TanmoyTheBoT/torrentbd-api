from torrentbd_api.login import login, check_login_status


def ensure_login():
    if not check_login_status():
        login()


def main():
    ensure_login()



if __name__ == "__main__":
    main()