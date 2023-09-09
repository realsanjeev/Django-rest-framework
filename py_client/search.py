import os
import requests
from auth import try_authentication

SECRET_FILE = "secret"

if os.path.exists(SECRET_FILE):
	with open(SECRET_FILE, 'r') as fp:
		token = fp.read()
else:
	token = try_authentication()
headers = {
	"Authorization": f"Bearer {token}"
}
endpoint = "http://localhost:8000/v4/api/search/"
query = input("Enter search query: ")
try:
	get_response = requests.get(endpoint, headers=headers, params={"q": query})
	print(get_response.json())
except:
	print("Error : err")

