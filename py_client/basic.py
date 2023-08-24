import requests

# HTTP requests endpoint
endpoint = "https://icanhazip.com"

get_requests = requests.get(endpoint)
get_response = requests.text # get raw response (Page source)