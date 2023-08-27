import requests
from getpass import getpass
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
    get_response = requests.put(endpoint, json=data, headers=headers)
    print(get_response.status_code)
except:
    print("Error while communication with endpoint")
