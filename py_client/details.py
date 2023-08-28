import os
import requests
from auth import try_authentication

SECRET_FILE = "secret"

endpoint = "http://localhost:8000/v2/api/1"

if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, "r") as fp:
        token = fp.read()
else:
    token = try_authentication()
headers = {
    "Authorization": f"Bearer {token}"
}

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

if __name__ == "__main__":
    get_response(endpoint, headers=headers)