import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

Authorization_URL = os.getenv("Authorization_URL")
api_key = os.getenv("API_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
API_URL = os.getenv("API_URL")

def get_cognito_token():
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(Authorization_URL + "token", headers=headers, data=json.dumps(payload))
    return response

def call_appsync_api_example(id_token):
    headers = {
        "Authorization": id_token
    }
    # GraphQLクエリ。例えば、GraphQLのqueryやmutationなど
    graphql_query = {
        "query": """query MyQuery {
            listDevices {
                items {
                    id
                    name
                    status
                }
            }
        }"""
    }
    response = requests.post(API_URL, json=graphql_query, headers=headers)
    return response.json()

# 実行例
auth_response = get_cognito_token()
if auth_response.status_code == 200:
    tokens = json.loads(auth_response.text)
    response = call_appsync_api_example(tokens["IdToken"])
    print(response)
else:
    print(auth_response)