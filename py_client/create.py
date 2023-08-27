import requests
from getpass import getpass

data = {"title": "Life is beautiful"}
endpoint = "http://localhost:8000/v2/api/"

# Auth begins
username = input("Ente your username: ")
password = getpass("Enter password: ")

auth_endpoint = "http://localhost:8000/v2/api/auth/"

get_auth = requests.post(auth_endpoint, data={"username": username,
                                         "password": password})

try:
    token = get_auth.json()["token"] or get_auth.json()["Bearer"]
    print("Auth token: ", token)
except:
    print("Auth Failed")
    exit()

headers = {
    "Authorization": f"Token {token}"
}

try:
    get_response = requests.post(endpoint, json=data, headers=headers)
    print("Post created response: ", get_response.json())
except:
    print("Error while creation of record in server")