import os
import requests
from auth import try_authentication
from json.decoder import JSONDecodeError

SECRET_FILE = "secret"
endpoint = "http://localhost:8000/v2/api/1"

# ---------------------------------------------------------
# Load or request token
# ---------------------------------------------------------
def load_token():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as fp:
            return fp.read().strip()
    return try_authentication()

token = load_token()
headers = {"Authorization": f"Bearer {token}"}

# ---------------------------------------------------------
# GET request helper
# ---------------------------------------------------------
def get_response(url_endpoint: str, params: dict = None, headers: dict = None, retry=True):
    print("*" * 45)
    print(f"{'-'*4} GET url: {url_endpoint} {'-'*4}")

    try:
        with requests.get(url_endpoint, params=params, headers=headers) as response:
            status = response.status_code

            # Retry authentication if token expired
            if status in (401, 403) and retry:
                print("Token expired or unauthorized. Re-authenticating...")
                new_token = try_authentication()
                headers["Authorization"] = f"Bearer {new_token}"
                return get_response(url_endpoint, params=params, headers=headers, retry=False)

            try:
                response_json = response.json()
                print("JSON response:", response_json)
                return response_json
            except JSONDecodeError:
                print("Non-JSON response received.")
                print("Status code:", status)
                print("Response text:", response.text)
                return response.text

    except requests.RequestException as e:
        print("Error during GET request:", e)
        return None

# ---------------------------------------------------------
# Run GET request
# ---------------------------------------------------------
if __name__ == "__main__":
    get_response(endpoint, headers=headers)
