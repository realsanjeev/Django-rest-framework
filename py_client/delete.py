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
