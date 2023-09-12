import os
import requests
from auth import try_authentication

SECRET_FILE = "secret"

# -----------------------------------------------------------
# Load saved token or authenticate
# -----------------------------------------------------------
def load_token():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as fp:
            return fp.read().strip()
    return try_authentication()

token = load_token()
headers = {"Authorization": f"Bearer {token}"}

# -----------------------------------------------------------
# Get book ID from user
# -----------------------------------------------------------
book_id = input("Enter ID of the book to delete: ")

try:
    book_id = int(book_id)
except ValueError:
    print(f"❌ '{book_id}' is not a valid numeric ID.")
    exit(1)

endpoint = f"http://localhost:8000/v2/api/{book_id}/"


# -----------------------------------------------------------
# Delete function with automatic token retry
# -----------------------------------------------------------
def delete_with_retry(url, headers, retry=True):
    response = requests.delete(url, headers=headers)

    # Retry if token is expired/invalid (401 or 403)
    if response.status_code in (401, 403) and retry:
        print("🔄 Token invalid. Re-authenticating...")
        new_token = try_authentication()
        headers["Authorization"] = f"Bearer {new_token}"
        return delete_with_retry(url, headers, retry=False)

    return response


# -----------------------------------------------------------
# Execute delete request
# -----------------------------------------------------------
try:
    response = delete_with_retry(endpoint, headers)

    print("\n----- Server Response -----")
    print(f"Status Code: {response.status_code}")

    try:
        print("JSON:", response.json())
    except Exception:
        print("Raw content:", response.content.decode("utf-8"))
    print("---------------------------\n")

except requests.RequestException as e:
    print("❌ Error communicating with server:")
    print(e)
