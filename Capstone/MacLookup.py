"""
MacLookup Library - code for pulling in OUI Table and checking MAC address against it
"""

from urllib.request import urlopen
import ssl
import re


class MacLookUpTableItem:

    """
    Initialization function __init__
    :param mac_oui (String)
    :param short_name (Strng)
    :param long_name (String)
    """
    def __init__(self, mac_oui, short_name,long_name):
        self.mac_oui = mac_oui
        self.short_name = short_name
        self.long_name = long_name

    def get_mac_oui(self):
        return self.mac_oui

    def get_short_name(self):
        return self.short_name

    def get_long_name(self):
        return self.long_name

class MacLookup:

    # Initializer
    # input validation on MAC
    #  convert MAC into ints and split to octets
    ###### - JKA

    """
    Initialization function __init__
    :param mac_address - (String) mac_address to match/search
    """
    def __init__(self, mac_address):
        self.lookup_item_list = []
        self.mac_address = self.convert_to_octets(mac_address)
        self.mac_address_oui = str(self.mac_address[0]) + ":" + str(self.mac_address[1]) + ":" + str(self.mac_address[2])

    def main(self):
        return 0

    def convert_to_octets(self, mac_address):
        hex_octets = []
        if self.how_many_char(":-", mac_address) != 0:
            octets = mac_address.replace("-", ":").split(":")
            for octet in octets:
                hex_octets.append(hex(int("0x" + octet, 16))[2:])
            return hex_octets
        else:
            print(mac_address)
            raise Exception('Mac address not properly formatted')

    """
    Retrieve OUI Table from wireshark website
    Only deal with 3 digit OUI for not
    Todo: - need to code for storage of 6 digit OUI and masks
    :return (Bool) True on success - else False
    """
    def retrieve_oui_table (self):
        ssl._create_default_https_context = ssl._create_unverified_context
        oui_table = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"

        for line in urlopen(oui_table):
            line_split = str(line, 'utf-8').split("\t")
            this_oui_instance = ""

            if len(line_split) == 3:
                if len(line_split[0]) < 9:
                    octets = self.convert_to_octets(line_split[0])
                    for octet in octets:
                        if len(this_oui_instance) == 0:
                            this_oui_instance = octet
                        else:
                            this_oui_instance = this_oui_instance + ":" + octet

                this_oui_instance = MacLookUpTableItem(line_split[0], line_split[1], line_split[2])
                self.lookup_item_list.append(this_oui_instance)

        print("loaded items from Wireshark list: " + str(len(self.lookup_item_list)))
        return True
    # def macLookup (self):
    #    pass

    def print_oui_reference(self):
        for item in self.lookup_item_list:
            print(item.mac_oui + " " + item.short_name)

    """
    Count how many times a character appears in a string
    Utility function - Todo - move to utility library
    :param char (String)
    :param input_string (String)
    :return int (Int) - number of matches - >0 - equal at least one match - 0 - none
    """
    def how_many_char(self, char, input_string):
        return len([x for x in input_string if x in char])

    """
    Lookup up Mac Address and return manufacturer
    
    """
    def mac_lookup(self):
        for item in self.lookup_item_list:
            if self.mac_address_oui.upper() == item.get_mac_oui().upper():
                print("Match Found: " + self.mac_address_oui + "<>" + item.get_mac_oui())
                print("Short Name: " + item.get_short_name())
                print("Long Name: " + item.get_long_name())
                return True
        print("Unknown MAC OUI")
        return False

    if __name__ == '__main__':
        main()

