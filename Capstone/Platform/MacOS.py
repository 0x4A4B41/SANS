import objc
import os
import pwd
import io
import re
import json

""" MacOS - platform specific code for scanning wifi - MacOS is first platform. Will write similar code segments for
Win32, Linux, and others """


class MacOS:
    """ Initialization function """
    def __init__(self):
        objc.loadBundle('CoreWLAN', globals(), bundle_path='/System/Library/Frameworks/CoreWLAN.framework')
        self.iface = CWInterface.interface()

    """ Scan Networks - scan for wireless networks
    :return result object """
    def scan_wifi(self):
        result, error = self.iface.scanForNetworksWithName_includeHidden_error_(None, True, None)
        return result

    @staticmethod
    def get_home_dir():
        return pwd.getpwuid(os.getuid()).pw_dir

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
    def read_from_file(filename, path):
        data = []
        filename = os.path.join(filename, path)
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

    @staticmethod
    def main():
        return 0

    if __name__ == '__main__':
        main()
