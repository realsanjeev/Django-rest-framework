import os
import json
import requests
from jwt_client import JWTClient

book_id = input("Enter id of book needed to delete: ")

try:
    book_id = int(book_id)
except:
    print(f"Book id {book_id} id not valid")
    book_id = None

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

endpoint = f"http://localhost:8000/v2/api/{book_id}/"
try:
    get_response = requests.delete(endpoint, headers=headers)
    print(get_response.content)
    print(get_response.status_code)
except:
    print("Error while communication with endpoint")
