""" Capstone WiFi Project - Main entry point
"""

from MacLookup import MacLookup
from Platform.MacOS import MacOS


class Main:

    def __init__(self):
        self.mac_lookup_obj = MacLookup()
        self.mac_lookup_obj.retrieve_oui_table_wireshark()
        self.mac_lookup_obj.retrieve_oui_table_nmap()

    """ Pre connect Scan Function"""
    def pre_connect_scan(self):
        platform_obj = MacOS()
        wifi_scan_results = platform_obj.scan_wifi()
        self.print_pre_connect_scan_results(wifi_scan_results)

    """ Print function for pre connect scan"""
    def print_pre_connect_scan_results(self, results):
        print("______________________")
        for result in results:
            print("SSID: " + str(result.ssid()))
            print("bssid: " + result.bssid())
            print("rssi: " + str(result.rssi()))
            print("channel: " + str(result.channel()))
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
