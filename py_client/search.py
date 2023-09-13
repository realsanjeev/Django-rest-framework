import os
import json
import requests
from jwt_client import JWTClient

endpoint = "http://localhost:8000/v4/api/search/"
query = input("Enter search query: ")

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
	get_response = requests.get(endpoint, headers=headers, params={"q": query})
	print(get_response.json())
except:
	print("Error : err")

