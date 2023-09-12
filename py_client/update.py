import os
import requests
from auth import try_authentication
from json.decoder import JSONDecodeError

SECRET_FILE = "secret"

# ---------------------------------------------------------
# Load token
# ---------------------------------------------------------
def load_token():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as fp:
            return fp.read().strip()
    return try_authentication()

token = load_token()
headers = {"Authorization": f"Bearer {token}"}

# ---------------------------------------------------------
# Get book ID
# ---------------------------------------------------------
book_id_input = input("Enter ID of book to update: ")

try:
    book_id = int(book_id_input)
except ValueError:
    print(f"❌ Book ID '{book_id_input}' is not valid.")
    exit(1)

endpoint = f"http://localhost:8000/v2/api/{book_id}/"

# ---------------------------------------------------------
# Data to update
# ---------------------------------------------------------
data = {
    "title": "FastAPI python",
    "desc": "It is nice while working with api",
    "price": 312.21
}

# ---------------------------------------------------------
# PUT request with retry for token expiration
# ---------------------------------------------------------
def update_book(url, json_data, headers, retry=True):
    try:
        with requests.put(url, json=json_data, headers=headers) as response:
            status = response.status_code

            # Retry if token expired
            if status in (401, 403) and retry:
                print("Token expired. Re-authenticating...")
                new_token = try_authentication()
                headers["Authorization"] = f"Bearer {new_token}"
                return update_book(url, json_data, headers, retry=False)

            print("Status code:", status)
            try:
                print("Response JSON:", response.json())
            except JSONDecodeError:
                print("Non-JSON response received:", response.text)

            return response.status_code

    except requests.RequestException as e:
        print("Error communicating with server:", e)
        return None

# ---------------------------------------------------------
# Execute update
# ---------------------------------------------------------
update_book(endpoint, data, headers)
