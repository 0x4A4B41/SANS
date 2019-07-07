from urllib.request import urlopen
import io
import os
import pwd
import re
import json
import ssl
import sys
"""
Common Objects
"""


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

class Printable:
    def __repr__(self):
        from pprint import pformat
        # return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)
        return str(self.__class__) + '\n' + '\n'.join(
            ('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

class Common:
    def __init__(self):
        self.lookup_item_list_nmap = []
        self.lookup_item_list_wireshark = []

    def get_app_data_dir(self):
        return os.path.join(self.get_home_dir(), '.capstone_data')

    @staticmethod
    def write_to_file(filename, path, data):
        filename = os.path.join(path, filename)
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
            f.flush()
            f.close()

    @staticmethod
    def get_home_dir():
        if sys.platform == "darwin":
            return pwd.getpwuid(os.getuid()).pw_dir
        if sys.platform == "win32":
            return os.path.expanduser(os.getenv('USERPROFILE'))
        else:
            return os.path.expanduser("~")

    @staticmethod
    def read_from_file(filename, path):
        filename = os.path.join(path, filename)
        with io.open(filename, 'r', encoding='utf-8') as f:
            data = f.readlines()
        return data

    @staticmethod
    def parse_oui_json(json_string):
        object_list = []
        json_objs = re.findall("({.*?})", json_string)
        for _object in json_objs:
            object_list.append(json.loads(_object))
        return object_list

    """ Count how many times a character appears in a string
    Utility function - Todo - move to utility library
    :param char (String)
    :param input_string (String)
    :return int (Int) - number of matches - >0 - equal at least one match - 0 - none """
    @staticmethod
    def how_many_char(char, input_string):
        return len([x for x in input_string if x in char])

    """
    OUI specific functions
    """

    """ Retrieve OUI Table from NMAP website
    Only deal with 3 digit OUI - no masks
    Todo: - need to code for storage of 6 digit OUI and masks
    :return (int) number of records imported """
    def retrieve_oui_table_nmap(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        oui_table = "https://linuxnet.ca/ieee/oui/nmap-mac-prefixes"
        for line in urlopen(oui_table):
            parts = str(line, 'utf-8').split("\t")  #tab-delimited data set
            if len(parts) == 2: # matches oui.txt format (0) MAC OUI (1) Vendor Short Name
                parts[0] = parts[0][0:2] + ":" + parts[0][2:4] + ":" + parts[0][4:6] #OUI
                self.lookup_item_list_nmap.append(MacLookUpTableItem(parts[0], parts[1]))
        return len(self.lookup_item_list_nmap)

    """ Retrieve OUI Table from wireshark website
    Only deal with 3 digit OUI for now
    Todo: - need to code for storage of 6 digit OUI and masks
    :return (int) number of records imported """
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
                self.lookup_item_list_wireshark.append(MacLookUpTableItem(parts[0], parts[1], parts[2]))
        return len(self.lookup_item_list_wireshark)

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
    @staticmethod
    def convert_nmap_to_octets(mac_address):
        hex_octets = []
        octets = [mac_address[0:2], mac_address[3:5], mac_address[6:8]]
        for octet in octets:
            hex_octets.append(hex(int("0x" + octet, 16))[2:])
        return hex_octets
