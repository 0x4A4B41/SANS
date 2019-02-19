"""
WigleConnector - Python Class to manage connecting to the Wigle.Net API
JKA
"""

# import json
import requests
# from requests.auth import HTTPBasicAuth


class WigleConnector:

    def __init__(self, api_name, api_token):
        self.api_name = api_name
        self.api_token = api_token

    def test_creds(self):
        test_url = "https://api.wigle.net/api/v2/profile/user"
        response = requests.get(test_url, auth=(self.api_name, self.api_token))
        data = response.json()
        if data['success'] == "true":
            return True
        return False

