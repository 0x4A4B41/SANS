""" Capstone WiFi Project - Main entry point
"""

from MacLookup import MacLookup
import sys
if sys.platform == "darwin":
    from Platform.MacOS import MacOS
elif sys.platform == "win32":
    from Platform.Win32 import Win32


class Main:

    def __init__(self):
        if sys.platform == "darwin":
            self.isMac = True
            self.isWin = False
            self.isLin = False
        elif sys.platform == "win32":
            self.isMac = False
            self.isWin = True
            self.isLin = False

        self.mac_lookup_obj = MacLookup()
        self.mac_lookup_obj.retrieve_oui_table_wireshark()
        self.mac_lookup_obj.retrieve_oui_table_nmap()

    """ Pre connect Scan Function"""
    def pre_connect_scan(self):
        print("pre_connect_scan_results enter")
        if self.isMac:
            platform_obj = MacOS()
        elif self.isWin:
            platform_obj = Win32()
        wifi_scan_results = platform_obj.scan_wifi()
        self.print_pre_connect_scan_results(wifi_scan_results)

    """ Print function for pre connect scan"""
    def print_pre_connect_scan_results(self, results):
        print("print_pre_connect_scan_results enter")
        if self.isWin:
            for result in results:
                    print("SSID:" + str(result.ssid))
                    for bssid in result.bssid:
                        if result.get_ssid() == bssid.get_ssid():
                            print("\tbssid:" + str(bssid.get_bssid()) + "\tsignal:" + str(bssid.get_signal()) + "\tchannel:" + str(bssid.get_channel()))
                            lookup_data = self.mac_lookup_obj.mac_lookup(bssid.get_bssid())
                            if type(lookup_data[0]) != int:
                                print("Short Name match (WireShark): " + str(lookup_data[0].get_short_name()))
                                print("Long Name match (WireShark): " + str(lookup_data[0].get_long_name()))
                            if type(lookup_data[1]) != int:
                                print("Short Name match (NMAP): " + lookup_data[1].get_short_name())
                            else:
                                print("Unable to find MAC OUI / BSSID")
                                print(lookup_data)
        elif self.isMac:
            for result in results:
                print("SSID: " + str(result.ssid()))
                print("\tbssid: " + result.bssid())
                print("\trssi: " + str(result.rssi()))
                print("\tchannel: " + str(result.channel()))
                lookup_data = self.mac_lookup_obj.mac_lookup(result.bssid())
                if type(lookup_data[0]) != int:
                    print("Short Name match (WireShark): " + str(lookup_data[0].get_short_name()))
                    print("Long Name match (WireShark): " + str(lookup_data[0].get_long_name()))
                if type(lookup_data[1]) != int:
                    print("Short Name match (NMAP): " + lookup_data[1].get_short_name())
                else:
                    print("Unable to lookup MAC OUI / BSSID")
                    print(lookup_data)

    def main(self):
        self.pre_connect_scan()

if __name__ == '__main__':
    _Main = Main()
    _Main.main()
