import os
import requests
from auth import try_authentication

SECRET_FILE = "secret"

# HTTP requests endpoint.
simple_endpoint = "http://localhost:8000/api/"
model_endpoint = "http://localhost:8000/api/product"

# REST_FRAMEWORK endpoints api responder
book_endpoint = "http://localhost:8000/v2/api/"

if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, "r") as fp:
        token = fp.read()
else:
    token = try_authentication()
headers = {
    "Authorization": f"Bearer {token}"
}

def get_response(url_endpoint: str,
                json: dict=None,
                params: dict=None,
                headers: dict=None):
    print("*"*45)
    print(f"{'*'*4}GET url: {url_endpoint}{'*'*4}")
    response = requests.get(url_endpoint,
                            params=params,
                            json=json,
                            headers=headers)
    status = response.status_code
    if status >= 400:
        try_authentication()

    page_source = response.text
    try:
        response_json = response.json()
        print("Json response: ", response_json)
    except requests.JSONDecodeError:
        print("response header: ", response.headers)
        print("response status: ", status)
    response.close()
    return None

def post_response(url_endpoint: str,
                json: dict=None,
                params: dict=None,
                data=None,
                headers: dict=None):
    print("*"*45)
    print(f"{'*'*4}POST url: {url_endpoint}{'*'*4}")
    response = requests.post(url_endpoint,
                            params=params,
                            json=json,
                            data=data,
                            headers=headers)
    status = response.status_code
    if status >= 400:
        print(f"{'-'*4}Auth needed{'-'*4}")
        try_authentication()
    page_source = response.text
    try:
        response_json = response.json()
        print("Json response: ", response_json)
    except requests.JSONDecodeError:
        print("response header: ", response.headers)
        print("response status: ", status)
    response.close()
    return None

# simple endpoint of django
# get_response(simple_endpoint, 
#              json={"message": "hello world"},
#              params={"q": "for sending param?q=search in url"}
#              )

# moodel endpoint. It is in api app
# get_response(model_endpoint)

# # new endpoint for book
get_response(book_endpoint, headers=headers)

# post to endpoint
post_response(book_endpoint,
              data={"title": "Work with api python"},
              headers=headers)