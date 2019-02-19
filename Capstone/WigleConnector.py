"""
WigleConnector - Python Class to manage connecting to the Wigle.Net API

Implements connector to parts of Wigle API needed for the application

JKA
"""

# import json
import requests
import urllib
# from requests.auth import HTTPBasicAuth


class WigleConnector:

    class WigleNetworkCommentRequest:
        request_url = "https://api.wigle.net/api/v2/network/comment"

        def __init__(self, api_name, api_token, network_id, comment):
            self.api_name = api_name
            self.api_token = api_token
            self.network_id = network_id
            self.comment = comment

        def send(self):
            response = requests.get(self.request_url, auth=(self.api_name, self.api_token))
            data = response.json()
            if data['success'] == "true":
                return True
            return False

    class WigleNetworkDetailRequest:
        # hardcoded to Wifi only - ignoring other net types
        ##########

        def __init__ (self, api_name, api_token, network_id, json_obj):
            self.api_name = api_name
            self.api_token = api_token
            self.network_id = network_id
            self.json_obj = json_obj
            self.network_type = "wifi"
            self.request_url = "https://api.wigle.net/api/v2/network/detail?netid=" + urllib.urlencode (self.network_id)

        def send(self):
            response = requests.get(request_url, auth=(self.api_name, self.api_token))
            data = response.json()
            if data['success'] == "true":
                return True
            return False

    class WigleNetworkGeoCodeRequest:
        pass

    class WigleNetworkSearchRequest:
        pass

    def __init__(self, api_name, api_token):
        self.api_name = api_name
        self.api_token = api_token

    def test_creds(self):
        request_url = "https://api.wigle.net/api/v2/profile/user"
        response = requests.get(request_url, auth=(self.api_name, self.api_token))
        data = response.json()
        if data['success'] == "true":
            return True
        return False

