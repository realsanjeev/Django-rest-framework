import os
import requests
from auth import try_authentication

SECRET_FILE = "secret"

data = {"title": "Life is beautiful"}
endpoint = "http://localhost:8000/v2/api/"

if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, "r") as fp:
        token = fp.read()
else:
    token = try_authentication()
headers = {
    "Authorization": f"Bearer {token}"
}


try:
    get_response = requests.post(endpoint, json=data, headers=headers)
    print("Post created response: ", get_response.json())
except:
    print("Error while creation of record in server")