import json
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dotenv import load_dotenv
import os

# 概要
# このプログラムは、agbeeAPIに接続するgqlライブラリを用いた最もシンプルなクライアントexampleです。
# 環境変数からAPIのアクセスに必要な情報を取得し、認証APIからトークンを取得します。
# 取得したトークンを使って、デバイスのリストを取得します。
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

# APIを呼び出す関数
def call_api_example(id_token):
    # GraphQLクエリ。例えば、デバイスのリストを取得するクエリ
    graphql_query = gql(
        """
        query ListDevices {
            listDevices {
                items {
                    id
                    name
                    status
                }
            }
        }
        """
    )

    # gqlクライアントの設定
    transport = RequestsHTTPTransport(
        url=API_URL,
        headers={"Authorization": id_token},
        use_json=True,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQLクエリの実行
    result = client.execute(graphql_query)
    return result

# 実行例
# 認証APIからトークンを取得
auth_response = get_token()
if auth_response.status_code == 200:
    # トークンの取得に成功した場合
    tokens = json.loads(auth_response.text)
    # 取得したトークンを使用してAppSync APIを呼び出す
    response = call_api_example(tokens["IdToken"])
    print(response)  # デバイスのリストを出力
else:
    # トークンの取得に失敗した場合
    print(auth_response)  # エラーメッセージを出力
