import subprocess
import re
import copy
""" Win32 - platform specific code for scanning wifi - MacOS is first platform. Will write similar code segments for
Linux, and others """


class BSSID:
    def __repr__(self):
        from pprint import pformat
        return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)

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



class WirelessNetwork:

    ssid=""
    auth=""
    bssid=[]

    def __repr__(self):
        from pprint import pformat
        return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)

    def __init__(self, *arg):
        line = re.sub("SSID [0-9].*: ", "", arg[0])  # SSID
        self.ssid = copy.copy(line)

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
            # print("result loop  (1): \n\n" + str(result))
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
        print("Win32: wrap_scan_wifi exit")
        print("Found " +str(len(self.ssids)) + " APs")
        return self.ssids


    def scan_wifi(self):
        print("Win32: scan_wifi entry")
        return self.wrap_scan_wifi(subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"]))
        #    print("_____(" + str(i) + ")")
        print("Win32: scan_wifi exit")

    @staticmethod
    def main():
        return 0

    if __name__ == '__main__':
        main()