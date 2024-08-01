import json
import requests
from urllib.parse import urlparse
from gql import gql, Client
from gql.transport.appsync_auth import AppSyncJWTAuthentication
from gql.transport.appsync_websockets import AppSyncWebsocketsTransport
from gql.transport.aiohttp import AIOHTTPTransport
from dotenv import load_dotenv
import os
import asyncio

# 概要
# このプログラムは、agbeeAPIに接続するgqlライブラリを用いたサブスクリプションのexampleです。
# agbeeがユーザーのボタン指示を待機している状態の検知を行います。
# プログラムの概要:
# - 認証APIからトークンを取得します。
# - 取得したトークンを使用して、非同期にタスクディスパッチを実行します。
# - asyncioを使用して非同期にバックグラウンドでサブスクリプションを行い、ActionInstanceの状態を監視します。
# - コールバック関数を設定して、特定の条件（WAITアクションでdurationSecが-1、resultがUNKNOWN）であることを検知します。
# 利用方法：
# - TaskDispatchのレスポンスで作成されたtaskInstanceとactionInstanceのIDを確認し、
#   agbee mockクライアントからActionInstanceの状態を変更することで、状態変更を検知します。
# - このプログラムは、Ctrl-Cでプログラムを終了します。
# - このプログラムを動かすには、.envファイルを編集して環境変数を設定する必要があります。

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

    result = data.get("onUpdateActionInstance").get("result")
    name = data.get("onUpdateActionInstance").get("action").get("name")
    actionType = data.get("onUpdateActionInstance").get("action").get("actionType")
    durationSec = data.get("onUpdateActionInstance").get("action").get("durationSec")

    if actionType == "WAIT" and durationSec == -1 and result == "UNKNOWN":
        print(f"agbeeがボタンが押されるまで待機しています")

# APIを呼び出す関数
async def dispatch_task_example(id_token):
    graphql_mutation = gql(
        """
        mutation TaskDispatch($input: TaskDispatchInput!) {
          taskDispatch(input: $input) {
            createdTaskInstances {
              id
              name
              status
              assignedDeviceId
              actions {
                items {
                  action {
                    actionType
                    name
                    durationSec
                  }
                  id
                }
              }
            }
            userErrors {
              message
              field
            }
          }
        }
        """
    )

    # gqlクライアントの設定
    transport = AIOHTTPTransport(
        url=API_URL,
        headers={"Authorization": id_token}
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # ミューテーションの実行
    params = {
        "input": {
            "expiredHour": 10,
            "reserveOnFailure": False,
            "tasks": {
                "description": "",
                "name": "",
                "actions": [{
                    "actionType": "WAIT",
                    "durationSec": 10,
                    "transitPoses": []
                },
                {
                    "actionType": "WAIT",
                    "durationSec": -1,
                    "transitPoses": []
                }]
            }
        }
    }
    result = await client.execute_async(graphql_mutation, variable_values=params)
    return result

# APIのサブスクリプションを呼び出す関数
async def subscribe_to_api(id_token):
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
        subscription OnUpdateActionInstance {
            onUpdateActionInstance {
                id
                result
                elapsedTime
                action {
                    name
                    actionType
                    durationSec
                }
            }
        }
        """
    )

    # サブスクリプションのストリームを受信するループ
    try:
        async for result in client.subscribe_async(subscription):
            on_message(result)
    except KeyboardInterrupt:
        print("Subscription interrupted by user. Exiting...")

# メイン関数
async def main():
    auth_response = get_token()
    if auth_response.status_code == 200:
        tokens = json.loads(auth_response.text)
        # サブスクリプションをバックグラウンドで実行
        subscription_task = asyncio.create_task(subscribe_to_api(tokens["IdToken"]))
        # タスクディスパッチを実行
        response = await dispatch_task_example(tokens["IdToken"])
        print(response)
        # サブスクリプションタスクが終了するのを待つ
        await subscription_task
    else:
        print(auth_response)

# メイン関数の実行
if __name__ == "__main__":
    asyncio.run(main())
