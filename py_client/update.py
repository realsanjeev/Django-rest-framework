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

book_id = input("Enter id of book needed to update: ")
data = {
    "title": "FastAPI python",
    "desc": "It is nice while working with api",
    "price": 312.21
}

try:
    book_id = int(book_id)
    endpoint = f"http://localhost:8000/v2/api/{book_id}/"
except:
    print(f"Book id {book_id} id not valid")
    endpoint = f"http://localhost:8000/v2/api/"

try:
    headers = client.get_headers()
    get_response = requests.put(endpoint, json=data, headers=headers)
    print(get_response.status_code)
except:
    print("[ERROR] Error while communication with endpoint")
