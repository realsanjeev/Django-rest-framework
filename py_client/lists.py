import requests

endpoint_parent = "http://localhost:8000/v2/api/"

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

get_response(endpoint_parent)
