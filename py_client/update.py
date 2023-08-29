import os
import requests
from auth import try_authentication

SECRET_FILE = "secret"
if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, "r") as fp:
        token = fp.read()
else:
    token = try_authentication()
headers = {
    "Authorization": f"Bearer {token}"
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
