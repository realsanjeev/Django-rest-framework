import requests

endpoint = "http://localhost:8000/v1/api/1"
endpoint_to_post = "http://localhost:8000/v1/api/"

def get_response(url_endpoint: str,
                json: dict=None,
                params: dict=None):
    print("*"*45)
    print(f"{'*'*4}GET url: {url_endpoint}{'*'*4}")
    response = requests.get(url_endpoint, params=params, json=json)
    status = response.status_code
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
                data=None):
    print("*"*45)
    print(f"{'*'*4}POST url: {url_endpoint}{'*'*4}")
    response = requests.post(url_endpoint, params=params, json=json, data=data)
    status = response.status_code
    page_source = response.text
    try:
        response_json = response.json()
        print("Json response: ", response_json)
    except requests.JSONDecodeError:
        print("response header: ", response.headers)
        print("response status: ", status)
    response.close()
    return None

# get_response(endpoint)
post_response(endpoint_to_post, json={"title": "Class post method 1"})