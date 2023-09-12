import json
from pathlib import Path
from dataclasses import dataclass
from getpass import getpass

import requests

@dataclass
class JWTClient:
    access: str =None
    refresh: str =None
    # ensure this matches simplejwt config
    header_type: str ="Bearer"
    base_endpoint: str ="http://localhost:8000/api"
    # file path is insecure
    cred_path: Path = Path("creds.json")

    def __post_init__(self):
        if self.cred_path.exists():
            try:
                data = json.loads(self.cred_path.read_text())
            except json.JSONDecodeError:
                print("JSON encoding error")
                data = None
            if data is None:
                '''
                Claer stored creds and
                Run login process
                '''
                self.clear_tokens()
                self.perform_auth()
            else:
                '''
                Verify token ->
                if necessary, Return token
                if necessary, Run login process
                '''
                self.access = data.get('access')
                self.refresh = data.get('refresh')
                token_verified = self.verify_token()
                if not token_verified:
                    """
                    This means token is invalid. attempt refresh
                    """
                    refreshed = self.perform_refresh()
                    if not refreshed:
                        """
                        token refresh also fialed. Run login process
                        """
                        print("Invalid data, REquire login again.")
                        self.clear_tokens()
                        self.perform_auth()
        else:
            self.perform_auth()
    
    def get_headers(self, header_type=None):
        _type = header_type or self.header_type
        token = self.access
        if not token:
            return {}
        return {
            "Authorization": f"{_type} {token}"
        }
    
    def perform_auth(self):
        endpoint = f"{self.base_endpoint}/token/"
        username = input("Enter your username: ")
        password = getpass("Enter password: ")
        req = requests.post(endpoint, json={"username": username, "password":password})
        if req.status_code != 200:
            raise requests.RequestException(f"Acess not granted: {req.text}")
        print("Access Granted")
        self.write_creds(req.json())
    
    def write_creds(self, data: dict):
        """
        Store the credentials in local file
        """
        if  self.cred_path is not None:
            self.access = data.get("access")
            self.refresh = data.get("refresh")
            if self.access and self.refresh:
                self.cred_path.write_text(json.dumps(data))
    
    def verify_token(self):
        data = {
            "token": f"{self.access}"
        }
        endpoint = f"{self.base_endpoint}/token/verify/"
        req = requests.post(endpoint, json=data)
        return req.status_code == 200
    
    def clear_tokens(self):
        self.access = None
        self.refresh = None
        if self.cred_path.exists():
            self.cred_path.unlink()
    
    def perform_refresh(self):
        print("[INFO] Refreshing Token...")
        headers = self.get_headers()
        data = {
            "refresh": f"{self.refresh}"
        }
        endpoint = f"{self.base_endpoint}/token/refresh/"
        req = requests.post(endpoint, data=data, headers=headers)
        if req.status_code != 200:
            self.clear_tokens()
            return False
        refresh_data = req.json()
        if not 'access' in refresh_data:
            self.clear_tokens()
            return False
        stored_data = {
            "access": refresh_data.get("access"),
            "refresh": self.refresh
        }
        self.write_creds(stored_data)
        return True
    
    def list(self, endpoint=None, page=1):
        headers = self.get_headers()
        if endpoint is None or self.base_endpoint not in str(endpoint):
            endpoint = f"{self.base_endpoint}/products/?page={page}"
        req = requests.get(endpoint, headers=headers)
        print("*"*10)
        print(req.json())
        print(headers)
        print("*"*10)
        if req.status_code != 200:
            raise requests.RequestException(f"Request failed: {req.text}")
        data = req.json()
        return data
    
if __name__ == "__main__":
    client = JWTClient()
    lookup_data = client.list()
    results = lookup_data.get("results")
    next_url = lookup_data.get("next")
    print(f'results: {results}')
    print("Next url: ", next_url)


