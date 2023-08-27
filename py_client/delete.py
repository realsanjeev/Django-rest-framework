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


book_id = input("Enter id of book needed to delete: ")

try:
    book_id = int(book_id)
except:
    print(f"Book id {book_id} id not valid")
    book_id = None


endpoint = f"http://localhost:8000/v2/api/{book_id}/"
try:
    get_response = requests.delete(endpoint, headers=headers)
    print(get_response.content)
    print(get_response.status_code)
except:
    print("Error while communication with endpoint")
