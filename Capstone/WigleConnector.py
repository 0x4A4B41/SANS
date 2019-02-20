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

        """
        Initialization function __init__
        :param api_name - (String) username for Wigle API
        :param api_token - (String) auth token for Wigle API
        :param network_id - (String) BSSID for wireless network
        :param comment - (String) comment
        """
        def __init__(self, api_name, api_token, network_id, comment):
            self.api_name = api_name
            self.api_token = api_token
            self.network_id = network_id
            self.comment = comment

        """
        API Send function shoots request to Wigle URL - uses values from init
        :return (Bool) - True on Success; False else
        """
        def send(self):
            response = requests.get(self.request_url, auth=(self.api_name, self.api_token))
            data = response.json()
            if data['success'] == "true":
                return True
            return False

    class WigleNetworkDetailRequest:
        # hardcoded to Wifi only - ignoring other net types
        ##########

        """
        Initialization function __init__
        :param api_name - (String) username for Wigle API
        :param api_token - (String) auth token for Wigle API
        :param network_id - (String) BSSID for wireless network
        :param json_obj - (Object) formed json_obj to be sent
        """
        def __init__(self, api_name, api_token, network_id, json_obj):
            self.api_name = api_name
            self.api_token = api_token
            self.network_id = network_id
            self.json_obj = json_obj
            self.network_type = "wifi"
            self.request_url = "https://api.wigle.net/api/v2/network/detail?netid=" + urllib.urlencode (self.network_id)

        """
        API Send function shoots request to Wigle URL - uses values from init
        :return (Bool) - True on Success; False else
        """
        def send(self):
            response = requests.get(self.request_url, auth=(self.api_name, self.api_token))
            data = response.json()
            if data['success'] == "true":
                return True
            return False

    class WigleNetworkGeoCodeRequest:
        # hardcoded to Wifi only - ignoring other net types
        ##########

        request_url = "https://api.wigle.net/api/v2/network/geocode"

        """
        Initialization function __init__
        :param api_name - (String) username for Wigle API
        :param api_token - (String) auth token for Wigle API
        :param address_code - (String) Address: Street, City, State/Region, Country
        """
        def __init__(self, api_name, api_token, address_code):
            self.api_name = api_name
            self.api_token = api_token
            self.address_code = address_code

        """
        API Send function shoots request to Wigle URL - uses values from init
        :return (Bool) - True on Success; False else
        """
        def send(self):
            response = requests.get(self.request_url, auth=(self.api_name, self.api_token))
            data = response.json()
            if data['success'] == "true":
                return True
            return False

    class WigleNetworkSearchRequest:
        pass

    """
            Initialization function __init__
            :param api_name - (String) username for Wigle API
            :param api_token - (String) auth token for Wigle API
    """
    def __init__(self, api_name, api_token):
        self.api_name = api_name
        self.api_token = api_token

    """
                Test Credentials function test_creds
                :return (Bool) - True on Success; False else
    """
    def test_creds(self):
        request_url = "https://api.wigle.net/api/v2/profile/user"
        response = requests.get(request_url, auth=(self.api_name, self.api_token))
        data = response.json()
        if data['success'] == "true":
            return True
        return False

