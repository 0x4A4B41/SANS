import subprocess
import re

""" Win32 - platform specific code for scanning wifi - MacOS is first platform. Will write similar code segments for
Linux, and others """

from ..Platform.Common import BSSID
from ..Platform.Common import WirelessNetwork


class Win32:

    def __init__(self):
        self.ssids = []

    def scan_wifi(self):
        result = bytearray(subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"])).decode()
        return self.wrap_scan_wifi(result)

    """ Scan Networks - scan for wireless networks
        :return result object """

    def wrap_scan_wifi(self, results):
        wireless_nets = []
        results_ = results.split("\nSSID")
        for result in results_:
            wn = WirelessNetwork(result)
            wnbssid = BSSID()  # new
            result = "SSID" + result
            result_ = result.split("\n")
            has_ssid = False
            has_bssid = False
            has_channel = False
            has_auth = False
            has_rssi = False
            for line in result_:
                if re.match("SSID [0-9].*: ", line):
                    line = re.sub("SSID [0-9].*: ", "", line)  # SSID
                    ssid = line.replace("\r", "").strip(" ")
                    wnbssid.set_ssid(ssid)
                    has_ssid = True
                elif re.match(".+Authentication.+: ", line):
                    line = re.sub("Authentication.*: ", "", line)  # Security
                    auth = line.replace("\r", "").strip(" ")
                    wn.set_auth(auth)
                    has_auth = True
                elif re.match(".+BSSID [0-9].*: ", line):
                    line = re.sub(".+BSSID [0-9].*: ", "", line)  # BSSID
                    bssid = line.replace("\r", "").strip(" ")
                    wnbssid.set_bssid(bssid)
                    has_bssid = True
                elif re.match(".+Signal.+: ", line):
                    line = line.replace('\r', '')
                    signal = re.sub("Signal.*:", "", line).strip(' ')  # RSSI
                    rssi = (int(signal.strip('%')) / 2) - 100
                    wnbssid.set_signal(str(rssi))
                    has_rssi = True
                elif re.match(".+Channel.+:.+", line):
                    line = re.sub("Channel.*:", "", line)  # ChannelNumber
                    channel = line.replace("\r", "").strip(" ")
                    wnbssid.set_channel(channel)
                    has_channel = True
#            wnbssid.set_bssid(bssid)
#            wnbssid.set_ssid(ssid)
#            wnbssid.set_channel(channel)
#            wn.set_ssid(ssid)
#            wn.set_auth(auth)
#            wn.set_bssid(wnbssid)
#            wireless_nets.append(wn)
            if has_auth & has_bssid & has_channel & has_ssid & has_rssi:
                net = dict({
                    'ssid': ssid,
                    'mac address': bssid,
                    'rssi': rssi,
                    'security': auth
                                           })
                wireless_nets.append(net)
        return wireless_nets

    """ scan_wifi function returns text output from netsh command (Windows 10)
    output is ugly - wrote wrapper to process output wrap_scan_wifi(input str)
    todo: Modify code to utilize API
    :return list of WirelessNetwork objects
    """

    @staticmethod
    def main():
        return 0

    if __name__ == '__main__':
        main()
