"""
MacLookup Library - code for pulling in OUI Table and checking MAC address against it
"""

from urllib.request import urlopen
import ssl


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

    """
    Returns MAC OUI
    :return String (mac_oui)
    """
    def get_mac_oui(self):
        return self.mac_oui

    """
    Returns Short Name
    :return String (short_name)
    """
    def get_short_name(self):
        return self.short_name

    """
    Returns Long Name
    :return String (long_name)
    """
    def get_long_name(self):
        return self.long_name

class MacLookup:
    """
    Initialization function __init__
    """
    def __init__(self):
        self.lookup_item_list = []

    def main(self):
        return 0

    """ Convert Mac Address String xx:xx:xx:yy:yy:yy | xx-xx-xx-yy-yy-yy
    to array of int/hex objects
    :param mac_address - MAC address string
    :return hex_octets - array/list of MAC octets
    :raise exception - 'Invalid MAC Address' """
    def convert_to_octets(self, mac_address):
        hex_octets = []
        if self.how_many_char(":-", mac_address) != 0:
            octets = mac_address.replace("-", ":").split(":")
            for octet in octets:
                hex_octets.append(hex(int("0x" + octet, 16))[2:])
            return hex_octets
        else:
            print(mac_address)
            raise Exception('Invalid MAC Address: Mac address not properly formatted')

    """ Retrieve OUI Table from wireshark website
    Only deal with 3 digit OUI for not
    Todo: - need to code for storage of 6 digit OUI and masks
    :return (Bool) True on success - else False """
    def retrieve_oui_table (self):
        ssl._create_default_https_context = ssl._create_unverified_context
        oui_table = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"

        for line in urlopen(oui_table):
            line_split = str(line, 'utf-8').split("\t")
            this_oui_instance = ""

            if len(line_split) == 3:        # validate data fits into MacLookupTableItem object
                if len(line_split[0]) < 9:  # expect xx:yy:zz - todo rewrite code to address MAC OUI with Masking
                    octets = self.convert_to_octets(line_split[0])
                    for octet in octets:
                        if len(this_oui_instance) == 0:
                            this_oui_instance = octet
                        else:
                            this_oui_instance = this_oui_instance + ":" + octet
                self.lookup_item_list.append(MacLookUpTableItem(line_split[0], line_split[1], line_split[2]))
        print("loaded items from WireShark list: " + str(len(self.lookup_item_list)))
        return True
    # def macLookup (self):
    #    pass

    def print_oui_reference(self):
        for item in self.lookup_item_list:
            print(item.mac_oui + " " + item.short_name)

    """ Count how many times a character appears in a string
    Utility function - Todo - move to utility library
    :param char (String)
    :param input_string (String)
    :return int (Int) - number of matches - >0 - equal at least one match - 0 - none """
    @staticmethod
    def how_many_char(char, input_string):
        return len([x for x in input_string if x in char])

    """ Lookup up Mac Address and return manufacturer
    :return MacLookupTableItem object for match or 0 """
    def mac_lookup(self, mac_address):
        mac_address = self.convert_to_octets(mac_address)
        mac_address_oui = str(mac_address[0]) + ":" + str(mac_address[1]) + ":" + str(mac_address[2])
        for item in self.lookup_item_list:
            if mac_address_oui.upper() == item.get_mac_oui().upper():
                return item
        print("Unknown MAC OUI")
        return 0

    if __name__ == '__main__':
        main()

