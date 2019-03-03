import objc
import os
import pwd
from .Common import Common


""" MacOS - platform specific code for scanning wifi - MacOS is first platform. Will write similar code segments for
Win32, Linux, and others """


class MacOS(Common):
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

    @staticmethod
    def main():
        return 0

    if __name__ == '__main__':
        main()
