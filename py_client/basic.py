import requests

# HTTP requests endpoint.
simple_endpoint = "http://localhost:8000/api/"
model_endpoint = "http://localhost:8000/api/product"

get_response = requests.get(simple_endpoint, json={"data": "Passed through request simple_endpoint"}, 
                            params={"q": "search param"})
get_text = get_response.text # get raw response (Page source)
status = get_response.status_code # get status code
header = get_response.headers
# print("header: ", header)
# print("Source Code: ", get_text)
print("Status: ", status)
print("json response: ", get_response.json())
print("*"*45)

product_response = requests.get(model_endpoint)
print("Random porduct response: ", product_response.json())

