import os
import requests
from auth import try_authentication
from json.decoder import JSONDecodeError

SECRET_FILE = "secret"
endpoint = "http://localhost:8000/v4/api/search/"

# --------------------------------------------------------
# Load token
# --------------------------------------------------------
def load_token():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as fp:
            return fp.read().strip()
    return try_authentication()

token = load_token()
headers = {"Authorization": f"Bearer {token}"}

# --------------------------------------------------------
# Search function with retry
# --------------------------------------------------------
def search(query, headers, retry=True):
    params = {"q": query}

    try:
        with requests.get(endpoint, headers=headers, params=params) as response:
            status = response.status_code

            # Retry authentication if token expired
            if status in (401, 403) and retry:
                print("Token expired or unauthorized. Re-authenticating...")
                new_token = try_authentication()
                headers["Authorization"] = f"Bearer {new_token}"
                return search(query, headers, retry=False)

            try:
                result = response.json()
                print("Search results:", result)
                return result
            except JSONDecodeError:
                print("Non-JSON response received:")
                print("Status code:", status)
                print("Response text:", response.text)
                return None

    except requests.RequestException as e:
        print("Error communicating with server:", e)
        return None

# --------------------------------------------------------
# MAIN
# --------------------------------------------------------
if __name__ == "__main__":
    query = input("Enter search query: ")
    search(query, headers)
