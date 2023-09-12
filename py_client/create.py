import os
import requests
from auth import try_authentication

SECRET_FILE = "secret"

data = {"title": "Life is beautiful"}
endpoint = "http://localhost:8000/v2/api/"

# ----------------------------------------------------
# Load or request token
# ----------------------------------------------------
def load_token():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as fp:
            return fp.read().strip()
    return try_authentication()

token = load_token()
headers = {"Authorization": f"Bearer {token}"}

# ----------------------------------------------------
# Send POST request with automatic retry
# ----------------------------------------------------
def post_with_retry(url, json_body, headers, retry=True):
    response = requests.post(url, json=json_body, headers=headers)
    
    # If token invalid (401/403), retry once
    if response.status_code in (401, 403) and retry:
        print("Token invalid. Re-authenticating...")
        new_token = try_authentication()
        headers["Authorization"] = f"Bearer {new_token}"
        return post_with_retry(url, json_body, headers, retry=False)

    # Attempt to parse JSON response
    try:
        return response.json()
    except Exception:
        print("Server returned non-JSON response:")
        print("Status:", response.status_code)
        print("Body:", response.text)
        return None

# ----------------------------------------------------
# MAIN CALL
# ----------------------------------------------------
try:
    print(f"Sending POST request to {endpoint}")
    json_response = post_with_retry(endpoint, data, headers)
    print("Post created response:", json_response)

except requests.RequestException as e:
    print("Error while creating record on the server:")
    print(e)
