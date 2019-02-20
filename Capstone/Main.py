"""
Capstone WiFi Project - Main entry point

"""

from MacLookup import MacLookup


ml = MacLookup("10:9a:dd:63:de:0d")
ml.retrieve_oui_table()
ml.mac_lookup()
