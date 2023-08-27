import requests
from getpass import getpass
# username = getuser() #get username of pc

username = input("Ente your username: ")
password = getpass("Enter password: ")

endpoint = "http://localhost:8000/v2/api/auth/"

get_auth = requests.post(endpoint, data={"username": username,
                                         "password": password})

try:
    token = get_auth.json()['token'] or get_auth.json()['Bearer']
    print("Auth response: ", get_auth.json())
except:
    print("Auth Failed")
