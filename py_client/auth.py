import os
import requests
from getpass import getpass

def try_authentication():
    username = input("Enter your username: ")
    password = getpass("Enter password: ")
    endpoint = "http://localhost:8000/v2/api/auth/"
    
    response = requests.post(endpoint, data={
        "username": username,
        "password": password
    })

    try:
        data = response.json()
    except ValueError:
        raise RuntimeError("Server did not return valid JSON.")

    if response.status_code != 200:
        raise RuntimeError(f"Auth failed: {data}")

    # Safely read either 'token' or 'Bearer'
    token = data.get("token") or data.get("Bearer")
    if not token:
        raise RuntimeError(f"Auth failed: no token in response {data}")

    with open("secret", "w") as file_handler:
        file_handler.write(token)

    print("Auth response:", data)
    return token


if __name__ == "__main__":
    try_authentication()
