import requests
import re


def GetLoginTokens() -> tuple:
    COOKIE_TOKEN = "__RequestVerificationToken"
    REGEX_HTML_TOKEN = re.compile("<input name=\"__RequestVerificationToken\" type=\"hidden\" value=\"(?P<token>.*?)\" />")

    r_top = requests.get("https://lightning.bitflyer.jp/")
    assert (r_top.status_code == 200)
    token_html = REGEX_HTML_TOKEN.search(r_top.text).group("token")
    token_cookie = r_top.cookies.get(COOKIE_TOKEN)
    return token_html, token_cookie


##############################

def Login(login_id, password, token_html, token_cookie) -> tuple:
    COOKIE_TOKEN = "__RequestVerificationToken"
    LOGIN_ID = login_id
    PASSWORD = password

    form_data = {
        "__RequestVerificationToken": token_html,
        "LoginId": LOGIN_ID,
        "Password": PASSWORD
    }
    # 二段階認証を適当に突破しているので，本当はここはもうちょっと丁寧にやる必要がある
    r_auth_1 = requests.post("https://lightning.bitflyer.jp/",
                             data=form_data,
                             cookies={COOKIE_TOKEN: token_cookie})
    assert r_auth_1.url == "https://lightning.bitflyer.jp/trade"

    session_1 = r_auth_1.history[0].cookies.get("ASP.NET_SessionId")
    session_2 = r_auth_1.history[1].cookies.get("api_session_v2")

    return session_1, session_2

    # r_auth_1 = requests.post("https://lightning.bitflyer.jp/",
    #                          data=form_data,
    #                          cookies={COOKIE_TOKEN: token_cookie},
    #                          allow_redirects=False)

    # assert r_auth_1.headers.get("Location") == "/Home/TwoFactorAuth"


