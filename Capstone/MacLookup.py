""" MacLookup Library - code for pulling in OUI Table and checking MAC address against it """

from urllib.request import urlopen
import ssl


class MacLookUpTableItem:

    """ Initialization function __init__
    :param mac_oui (String)
    :param short_name (Strng)
    :param long_name (String) """
    def __init__(self, *args):
        if len (args) == 3:
            self.mac_oui = str(args[0])
            self.short_name = str(args[1])
            self.long_name = str(args[2])
        if len (args) == 2:
            self.mac_oui = str(args[0])
            self.short_name = str(args[1])
            self.long_name = str(args[1])

    """ Returns MAC OUI
    :return String (mac_oui) """
    def get_mac_oui(self):
        return self.mac_oui

    """ Returns Short Name
    :return String (short_name) """
    def get_short_name(self):
        return self.short_name

    """ Returns Long Name
    :return String (long_name) """
    def get_long_name(self):
        return self.long_name


class MacLookup:
    """ Initialization function __init__ """
    def __init__(self):
        self.lookup_item_list = []
        self.lookup_item_list_nmap = []

    """ Placeholder """
    @staticmethod
    def main():
        return 0

    """ Convert Mac Address String xx:xx:xx:yy:yy:yy | xx-xx-xx-yy-yy-yy
    to array of int/hex objects - specific to data from wireshark
    :param mac_address - MAC address string
    :raise exception - 'Invalid MAC Address' """
    def convert_wireshark_to_octets(self, mac_address):
        hex_octets = []
        if self.how_many_char(":-", mac_address) != 0:
            octets = mac_address.replace("-", ":").split(":")
            for octet in octets:
                hex_octets.append(hex(int("0x" + octet, 16))[2:])
            return hex_octets
        else:
            print(mac_address)
            raise Exception('Invalid MAC Address: Mac address not properly formatted')

    """ Convert Mac Address String xx:xx:xx:yy:yy:yy | xx-xx-xx-yy-yy-yy
    to array of int/hex objects - specific to data from NMAP
    :param mac_address - MAC address string
    :raise exception - 'Invalid MAC Address' """
    def convert_nmap_to_octets(self, mac_address):
        hex_octets = []
        octets = [mac_address[0:2], mac_address[3:5], mac_address[6:8]]
        for octet in octets:
            hex_octets.append(hex(int("0x" + octet, 16))[2:])
        return hex_octets

    """ Retrieve OUI Table from NMAP website
    Only deal with 3 digit OUI - no masks
    Todo: - need to code for storage of 6 digit OUI and masks
    :return (Bool) True on success - else False """
    def retrieve_oui_table_nmap(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        oui_table = "https://linuxnet.ca/ieee/oui/nmap-mac-prefixes"
        for line in urlopen(oui_table):
            parts = str(line, 'utf-8').split("\t")
            if len(parts) == 2: # matches oui.txt format (0) MAC OUI (1) Vendor Short Name
                parts[0] = parts[0][0:2] + ":" + parts[0][2:4] + ":" + parts[0][4:6]
                self.lookup_item_list_nmap.append(MacLookUpTableItem(parts[0], parts[1]))
        print("loaded items from NMAP list: " + str(len(self.lookup_item_list_nmap)))

    """ Retrieve OUI Table from wireshark website
    Only deal with 3 digit OUI for now
    Todo: - need to code for storage of 6 digit OUI and masks
    :return (Bool) True on success - else False """
    def retrieve_oui_table_wireshark(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        oui_table = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"
        for line in urlopen(oui_table):
            parts = str(line, 'utf-8').split("\t")
            this_oui_instance = ""
            if len(parts) == 3:        # validate data fits into MacLookupTableItem object
                if len(parts[0]) < 9:  # expect xx:yy:zz - todo rewrite code to address MAC OUI with Masking
                    octets = self.convert_wireshark_to_octets(parts[0])
                    for octet in octets:
                        if len(this_oui_instance) == 0:
                            this_oui_instance = octet
                        else:
                            this_oui_instance = this_oui_instance + ":" + octet
                self.lookup_item_list.append(MacLookUpTableItem(parts[0], parts[1], parts[2]))
        print("loaded items from WireShark list: " + str(len(self.lookup_item_list)))

    """ Count how many times a character appears in a string
    Utility function - Todo - move to utility library
    :param char (String)
    :param input_string (String)
    :return int (Int) - number of matches - >0 - equal at least one match - 0 - none """
    @staticmethod
    def how_many_char(char, input_string):
        return len([x for x in input_string if x in char])

    def mac_lookup(self, mac_address_string):
        lookup_result = []
        mac_address_octets_wireshark = self.convert_wireshark_to_octets(mac_address_string)
        lookup_result.append(self.mac_lookup_match(self.lookup_item_list,mac_address_octets_wireshark))
        mac_address_octets_nmap = self.convert_nmap_to_octets(mac_address_string)
        lookup_result.append(self.mac_lookup_match(self.lookup_item_list_nmap, mac_address_octets_nmap))
        return lookup_result

    """ Lookup up Mac Address and return manufacturer
    :param local_lookup_list - array of lookup objects
    :param mac_address (String)
    :return MacLookupTableItem object for match or 0 """
    @staticmethod
    def mac_lookup_match(local_lookup_list, mac_address):
        mac_address_oui = str(mac_address[0]) + ":" + str(mac_address[1]) + ":" + str(mac_address[2])
        for item in local_lookup_list:
            if mac_address_oui.upper() == item.get_mac_oui().upper():
                return item
        return 0

    if __name__ == '__main__':
        main()

