"""
Capstone WiFi Project - Main entry point

"""

from MacLookup import MacLookup
from Platform.MacOS import MacOS


ml = MacLookup()
ml.retrieve_oui_table()
# ml.mac_lookup("10:9a:dd:63:de:0d")

m = MacOS()
results = m.scan_wifi()
for result in results:
    # print(result)
    print("SSID: " + str(result.ssid()))
    print("bssid: " + result.bssid())
    print("rssi: " + str(result.rssi()))
    print("channel: " + str(result.channel()))
    print("//////////////////////")
    mac_lookup_data = ml.mac_lookup(result.bssid())
    if type(mac_lookup_data) != int:
        print("Short Name match: " + str(mac_lookup_data.get_short_name()))
        print("Long Name match: " + str(mac_lookup_data.get_long_name()))
        print("______________________")
    else:
        print("Unable to lookup MAC OUI / BSSID")
        print("______________________")
