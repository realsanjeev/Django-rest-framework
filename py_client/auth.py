import os
import requests
from getpass import getpass
# username = getuser() #get username of pc

def try_authentication():
    username = input("Ente your username: ")
    password = getpass("Enter password: ")
    endpoint = "http://localhost:8000/v2/api/auth/"
    
    get_auth = requests.post(endpoint, data={"username": username,
                                            "password": password})

    try:
        token = get_auth.json()['token'] or get_auth.json()['Bearer']
        with open("secret", "w") as file_handler:
            file_handler.write(token)
        print("Auth response: ", get_auth.json())
        return token
    except Exception as err:
        raise f"Auth fail: {err}"

if __name__=="__main__":
    try_authentication()