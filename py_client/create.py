import requests

data = {"title": "Life is beautiful"}
endpoint = "http://localhost:8000/v1/api/create/"

try:
    get_response = requests.post(endpoint, json=data)
    print("Post created response: ", get_response.json())
except:
    print("Error while creation of record in server")