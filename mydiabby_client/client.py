import requests
from .exceptions import AuthenticationError, APIError


class MyDiabbyClient:

    def __init__(self,
                 username: str,
                 password: str,
                 base_url: str ="https://app.mydiabby.com/api"):
        
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None

        self._authenticate()


    def _authenticate(self):
        """Authenticate with MyDiabby and store Bearer token."""
        
        url = f"{self.base_url}/getToken/"
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


    def _request(self,
                 method: str,
                 endpoint: str, **kwargs):
        """Internal helper to call API with auto-refresh on 401."""
        url = f"{self.base_url}{endpoint}"
        resp = self.session.request(method, url, **kwargs)

        if resp.status_code == 401:
            # re-authenticate and retry once
            self._authenticate()
            resp = self.session.request(method, url, **kwargs)

        if not resp.ok:
            raise APIError(f"API error {resp.status_code}: {resp.text}")

        try:
            response = resp.json()
        except requests.JSONDecodeError:
            raise APIError("Invalid JSON response")

        return response


    def get_account(self):
        """Fetch account info."""
        return self._request("GET", "/account/")


    def get_data(self):
        """Fetch all diabetes data."""
        return self._request("GET", "/data/")
