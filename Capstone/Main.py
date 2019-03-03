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
        wireshark_records = self.mac_lookup_obj.retrieve_oui_table_wireshark()
        nmap_records = self.mac_lookup_obj.retrieve_oui_table_nmap()
        print("Loaded " + str(wireshark_records) + "+ records from Wireshark data")
        print("Loaded " + str(nmap_records) + "+ records from NMAP data")
        # todo: remove hardcoding for json file names
        self.write_oui_records_to_json(self.mac_lookup_obj.return_lookup_item_list_json(
                                        self.mac_lookup_obj.lookup_item_list),
                                       "wsharkoui.json")
        self.write_oui_records_to_json(self.mac_lookup_obj.return_lookup_item_list_json(
                                        self.mac_lookup_obj.lookup_item_list_nmap),
                                       "nmapoui.json")

    def write_oui_records_to_json(self, record_list_string, _filename):
        if self.isMac:
            platform_obj = MacOS()
        elif self.isWin:
            platform_obj = Win32()
        else:
            return -1
        platform_obj.write_to_file(_filename,
                                    platform_obj.get_app_data_dir(),
                                    record_list_string)
        return 0

    """ Pre connect Scan Function"""
    def pre_connect_scan(self):
        if self.isMac:
            platform_obj = MacOS()
        elif self.isWin:
            platform_obj = Win32()
        wifi_scan_results = platform_obj.scan_wifi()
        self.print_pre_connect_scan_results(wifi_scan_results)

    """ Print function for pre connect scan"""
    def print_pre_connect_scan_results(self, results):
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
        pass
        #self.pre_connect_scan()


if __name__ == '__main__':
    _Main = Main()
    _Main.main()
