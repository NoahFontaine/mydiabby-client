import requests
from .exceptions import AuthenticationError, APIError
from typing import Any


class MyDiabbyClient:

    def __init__(self,
                 username: str,
                 password: str,
                 base_url: str ="https://app.mydiabby.com/api"
                 ) -> None:
        
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None

        self.__authenticate()


    def __authenticate(self) -> None:
        """
        Authenticates with MyDiabby and stores the Bearer token."""
        
        url = f"{self.base_url}/getToken"
        payload = {"username": self.username,
                   "password": self.password,
                   "platform": "dt"}
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json, text/plain, */*"}

        resp = self.session.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            raise AuthenticationError(f"Failed to authenticate: {resp.text}")

        try:
            data = resp.json()
        except requests.JSONDecodeError:
            raise AuthenticationError("Invalid JSON response")

        self.token = data.get("token")
        if not self.token:
            raise AuthenticationError("No token in response")

        self.session.headers.update({"Authorization": f"Bearer {self.token}"})


    def __request(self,
                 method: str,
                 endpoint: str, **kwargs) -> Any:
        """
        Helper function that makes the necessary requests.
        If a 401 error code occurs, it will re-authenticate and retry once.
        """
        url = f"{self.base_url}{endpoint}"
        resp = self.session.request(method, url, **kwargs)

        if resp.status_code == 401:
            # re-authenticate and retry once
            self.__authenticate()
            resp = self.session.request(method, url, **kwargs)

        if not resp.ok:
            raise APIError(f"API error {resp.status_code}: {resp.text}")

        try:
            response = resp.json()
        except requests.JSONDecodeError:
            raise APIError("Invalid JSON response")

        return response


    def get_account(self) -> Any:
        """
        Fetch info about the user, as a json.
        """
        return self.__request("GET", "/account")


    def get_data(self) -> Any:
        """
        Fetch all CGM and pump data, as a json.
        """
        return self.__request("GET", "/data")
