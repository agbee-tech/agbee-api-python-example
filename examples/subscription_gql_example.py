import json
import requests
from urllib.parse import urlparse
from gql import gql, Client
from gql.transport.appsync_auth import AppSyncJWTAuthentication
from gql.transport.appsync_websockets import AppSyncWebsocketsTransport
from dotenv import load_dotenv
import os

# 概要
# このプログラムは、agbeeAPIに接続するgqlライブラリを用いたサブスクリプションのexampleです。
# 環境変数からAPIのアクセスに必要な情報を取得し、認証APIからトークンを取得します。
# 取得したトークンを使って、デバイスの状態変更をサブスクリプションで受信します。
# コールバック関数を設定して、取得した情報をプリントし、NEED_SUPPORTの状態を検知します。
# このプログラムは、Ctrl-Cでプログラムを終了します。
# このプログラムを動かすには、.envファイルを編集して環境変数を設定する必要があります。


# .envファイルをロードして環境変数を利用可能にする
load_dotenv()

# 環境変数から各種URLや認証情報を取得
Authorization_URL = os.getenv("Authorization_URL")
api_key = os.getenv("API_KEY")
USERNAME = os.getenv("ACCOUNT_ID")
PASSWORD = os.getenv("PASSWORD")
API_URL = os.getenv("API_URL")

# 認証トークンを取得する関数
def get_token():
    headers = {
        "x-api-key": api_key,  # APIキーをヘッダーに設定
        "Content-Type": "application/json",  # コンテンツタイプをJSONに設定
    }
    payload = {
        "username": USERNAME,  # ユーザー名をペイロードに設定
        "password": PASSWORD  # パスワードをペイロードに設定
    }
    response = requests.post(Authorization_URL + "token", headers=headers, data=json.dumps(payload))
    return response

# サブスクリプションでデータを受信したときのコールバック関数
def on_message(data):
    print("Received data:", data)

    status = data.get("onUpdateDevice").get("status")
    name = data.get("onUpdateDevice").get("name")

    if status == "NEED_SUPPORT":
        print(f"{name}の異常を検知しました")

# APIのサブスクリプションを呼び出す関数
def subscribe_to_api(id_token):
    ws_url = API_URL.replace("https", "wss") + "/realtime"
    # Extract host from url
    host = str(urlparse(ws_url).netloc)
    print(f"Host: {host}")

    auth = AppSyncJWTAuthentication(
        host=host,
        jwt=id_token,
    )
    transport = AppSyncWebsocketsTransport(
        url=ws_url,
        auth=auth,
    )
    client = Client(transport=transport)

    subscription = gql(
        """
        subscription OnUpdateDevice {
            onUpdateDevice {
                id
                name
                status
                temperature
                updatedAt
            }
        }
        """
    )

    # サブスクリプションのストリームを受信するループ
    try:
        for result in client.subscribe(subscription):
            on_message(result)
    except KeyboardInterrupt:
        print("Subscription interrupted by user. Exiting...")


# メイン関数
def main():
    auth_response = get_token()
    if auth_response.status_code == 200:
        tokens = json.loads(auth_response.text)
        subscribe_to_api(tokens["IdToken"])
    else:
        print(auth_response)

# メイン関数の実行
if __name__ == "__main__":
    main()
