import os
import json
import requests
from jwt_client import JWTClient

client = JWTClient()
SECRET_FILE = "creds.json"
client = JWTClient()
if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, "r") as fp:
        content = fp.read()
    token = json.loads(content)["access"]
    headers = {
        "Authorization": f"Bearer {token}"
    }
else:
    headers = client.get_headers()

endpoint_parent = "http://localhost:8000/v2/api/"

def get_response(url_endpoint: str,
                json: dict=None,
                params: dict=None,
                headers: dict=None):
    print("*"*45)
    print(f"{'*'*4}GET url: {url_endpoint}{'*'*4}")
    response = requests.get(url_endpoint, params=params, json=json, headers=headers)
    status = response.status_code
    page_source = response.text
    try:
        response_json = response.json()
        print("Json response: ", response_json)
    except requests.JSONDecodeError:
        print("response header: ", response.headers)
        print("response status: ", status)
    response.close()
    return None

if __name__=="__main__":
    get_response(endpoint_parent, headers=headers)
