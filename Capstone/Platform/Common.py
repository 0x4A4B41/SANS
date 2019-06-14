import io
import os
import re
import json

"""
Common Objects
"""


class Printable:
    def __repr__(self):
        from pprint import pformat
        # return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)
        return str(self.__class__) + '\n' + '\n'.join(
            ('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


class Common:

    def get_app_data_dir(self):
        return os.path.join(self.get_home_dir(), '.capstone_data')

    @staticmethod
    def write_to_file(filename, path, data):
        filename = os.path.join(path, filename)
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
            f.flush()
            f.close()

    @staticmethod
    def read_from_file(filename, path):
        filename = os.path.join(path, filename)
        with io.open(filename, 'r', encoding='utf-8') as f:
            data = f.readlines()
        return data

    @staticmethod
    def parse_oui_json(json_string):
        object_list = []
        json_objs = re.findall("({.*?})", json_string)
        for _object in json_objs:
            object_list.append(json.loads(_object))
        return object_list


""" Class for managing BSSID data - made a separate class because there can be a many-to-one relationship between SSIDs 
and BSSIDS - multiple APs attached to a network with a single SSID (Mesh)
:param  Printable
"""


class BSSID(Printable, Common):
    def __init__(self):
        self.bssid = ""
        self.ssid = ""
        self.channel = ""
        self.signal = ""

    def set_bssid (self, bssid):
        self.bssid = bssid

    def get_bssid(self):
        return self.bssid

    def set_ssid(self, ssid):
        self.ssid = ssid

    def get_ssid(self):
        return self.ssid

    def set_channel(self, channel):
        self.channel = channel

    def get_channel(self):
        return self.signal

    def set_signal(self, signal):
        self.signal = signal

    def get_signal(self):
        return self.signal


"""  Class for managing SSID data - m
:param  Printable
"""


class WirelessNetwork(Printable):

    def __init__(self, *arg):
        self.ssid = re.sub("SSID [0-9].*: ", "", arg[0])  # SSID
        self.auth = ""
        self.bssid = []

    def set_ssid(self, ssid):
        self.ssid = copy.copy(ssid)

    def get_ssid(self):
        return self.ssid

    def set_auth(self, auth):
        self.auth = auth

    def get_auth(self):
        return self.auth

    def set_bssid(self, bssid):
        self.bssid.append(bssid)

    def return_bssid(self):
        return self.bssid


