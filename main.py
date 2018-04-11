import sys
from subprocess import run, PIPE

from lib.get_session import GetLoginTokens, Login


def main():
    id = sys.argv[1]
    password = sys.argv[2]
    token_html, token_cookie = GetLoginTokens()
    ASP_NET_SessionId, api_session_v2 = Login(id, password, token_html, token_cookie)
    print(ASP_NET_SessionId, api_session_v2)
    # 例えばcURLなんかでも接続できる
    cmd = "curl https://lightning.bitflyer.jp/trade  -b api_session_v2={} -b ASP.Net_SessionId={}".format(api_session_v2, ASP_NET_SessionId)
    print(cmd)
    obj = run(cmd, stdout=PIPE, shell=True)
    print(obj.stdout.decode("utf-8"))

if __name__ == "__main__":
    main()
