# this is authentication for custom token auth using rest framework not for simple-jwt .
# So this doesnot work for project require simple-jwt as authentication in api
# See previous branch for this to work
import os
import requests
from getpass import getpass
# username = getuser() #get username of pc

SECRET_FILE = "secret"
def try_authentication():
    username = input("Ente your username: ")
    password = getpass("Enter password: ")
    endpoint = "http://localhost:8000/v2/api/auth/"
    
    get_auth = requests.post(endpoint,
                             data={"username": username,
                                    "password": password})

    try:
        token = get_auth.json()['token'] or get_auth.json()['Bearer']
        with open(SECRET_FILE, "w") as file_handler:
            file_handler.write(token)
        print("Auth response: ", get_auth.json())
        return token
    except Exception as err:
        raise f"Auth fail: {err}"

if __name__=="__main__":
    try_authentication()