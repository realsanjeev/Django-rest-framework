import os
import requests
from auth import try_authentication

SECRET_FILE = "secret"

# HTTP request endpoints
simple_endpoint = "http://localhost:8000/api/"
model_endpoint = "http://localhost:8000/api/product"
book_endpoint = "http://localhost:8000/v2/api/"


def load_token():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as fp:
            return fp.read().strip()
    return try_authentication()


token = load_token()
auth_headers = {"Authorization": f"Bearer {token}"}


def get_response(url_endpoint: str,
                 json: dict = None,
                 params: dict = None,
                 headers: dict = None):
    print("*" * 45)
    print(f"---- GET url: {url_endpoint} ----")

    response = requests.get(
        url_endpoint,
        params=params,
        json=json,
        headers=headers
    )

    status = response.status_code
    if status >= 400:
        print("Authentication might be required…")
        try_authentication()

    try:
        response_json = response.json()
        print("JSON response:", response_json)
        return response_json
    except requests.JSONDecodeError:
        print("Response headers:", response.headers)
        print("Response status:", status)
        print("Response text:", response.text)
        return None
    finally:
        response.close()


def post_response(url_endpoint: str,
                  json: dict = None,
                  params: dict = None,
                  data: dict = None,
                  headers: dict = None):
    print("*" * 45)
    print(f"---- POST url: {url_endpoint} ----")

    response = requests.post(
        url_endpoint,
        params=params,
        json=json,
        data=data,
        headers=headers
    )

    status = response.status_code
    if status >= 400:
        print("---- Auth needed ----")
        try_authentication()

    try:
        response_json = response.json()
        print("JSON response:", response_json)
        return response_json
    except requests.JSONDecodeError:
        print("Response headers:", response.headers)
        print("Response status:", status)
        print("Response text:", response.text)
        return None
    finally:
        response.close()


# GET request to book endpoint
get_response(book_endpoint, headers=auth_headers)

# POST request to book endpoint
post_response(
    book_endpoint,
    data={"title": "Work with api python"},
    headers=auth_headers
)
