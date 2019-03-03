import subprocess
import re
import copy
from .Common import Printable
from .Common import Common

""" Win32 - platform specific code for scanning wifi - MacOS is first platform. Will write similar code segments for
Linux, and others """


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
        line = re.sub("SSID [0-9].*: ", "", arg[0])  # SSID
        self.ssid = copy.copy(line)
        self.auth = ""
        self.bssid = []

    def set_ssid(self, ssid):
        self.ssid = copy.copy(ssid)

    def get_ssid(self):
        return self.ssid

    def set_auth(self, auth):
        self.auth = copy.copy(auth)

    def get_auth(self):
        return self.auth

    def set_bssid(self, bssid):
        self.bssid.append(copy.copy(bssid))

    def return_bssid(self):
        return self.bssid


""" Win32 Windows specific code
"""


class Win32:

    def __init__(self):
        self.ssids = []

    """ Scan Networks - scan for wireless networks
        :return result object """

    def wrap_scan_wifi(self, results):
        print("Win32: wrap_scan_wifi entry")
        results = results.decode()
        results_ = results.split("\nSSID")
        this_ssid = WirelessNetwork("")
        this_bssid = BSSID()
        for result in results_:
            result = "SSID" + result
            result_ = result.split("\n")
            for line in result_:
                if re.match("SSID [0-9].*: ", line):
                    if len(this_ssid.ssid) > 0:
                        self.ssids.append(this_ssid)
                        this_ssid = WirelessNetwork(line)
                        this_ssid.set_auth(str(this_ssid.auth))
                    else:
                        line = re.sub("SSID [0-9].*: ", "", line)  # SSID
                        this_ssid = WirelessNetwork(line)
                elif re.match(".+Authentication.+: ", line):
                    line = re.sub("Authentication.*: ", "", line)  # Security
                    this_ssid.set_auth(line.replace("\r", ""))
                elif re.match(".+BSSID [0-9].*: ", line):
                    if len(this_bssid.get_bssid()) > 0:
                        this_ssid.bssid.append(this_bssid)
                        this_bssid = BSSID()
                    line = re.sub(".+BSSID [0-9].*: ", "", line)  # BSSID
                    this_bssid.set_ssid(this_ssid.ssid)
                    this_bssid.set_bssid(line.replace("\r"," "))
                elif re.match(".+Signal.+: ", line):
                    line = re.sub("Signal.*:", "", line)  # RSSI
                    this_bssid.set_signal(line.replace("\r", ""))
                elif re.match(".+Channel.+:.+", line):
                    line = re.sub("Channel.*:", "", line)  # ChannelNumber
                    this_bssid.set_channel(line.replace("\r", ""))
        return self.ssids

    """ scan_wifi function returns text output from netsh command (Windows 10)
    output is ugly - wrote wrapper to process output wrap_scan_wifi(input str)
    todo: Modify code to utilize API
    :return list of WirelessNetwork objects
    """

    def scan_wifi(self):
        return self.wrap_scan_wifi(subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"]))

    @staticmethod
    def main():
        return 0

    if __name__ == '__main__':
        main()