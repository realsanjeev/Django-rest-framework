import os
import json
import requests
from jwt_client import JWTClient

title = input("Enter title: ")
body = input("Enter body: ")
data = {"title": title, "body": body}
endpoint = "http://localhost:8000/v2/api/"

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

try:
    get_response = requests.post(endpoint, json=data, headers=headers)
    print("Post created response: ", get_response.json())
except:
    print("[ERROR] Error while creation of record in server")