import objc
import os
import pwd

from ..Platform.Common import BSSID
from ..Platform.Common import WirelessNetwork

""" MacOS - platform specific code"""


class MacOS():
    """ Initialization function """
    def __init__(self):
        objc.loadBundle('CoreWLAN', globals(), bundle_path='/System/Library/Frameworks/CoreWLAN.framework')
        self.iface = CWInterface.interface()

    """ Scan Networks - scan for wireless networks
    :return result object """
    def scan_wifi(self):
        results, errors = self.iface.scanForNetworksWithName_includeHidden_error_(None, True, None)
        for result in results:
            # print (result)
            wnbssid = BSSID()
            wnbssid.set_bssid(str(result.bssid()))
            wnbssid.set_ssid(str(result.ssid()))
            wnbssid.set_channel(str(result.channel()))
            wn = WirelessNetwork(str(result.ssid()))
            wn.set_auth("")
            wn.set_bssid(wnbssid)
            print("SSID: " + str(result.ssid()))
            print("\tbssid: " + result.bssid())
            print("\trssi: " + str(result.rssi()))
            print("\tchannel: " + str(result.channel()))
            # print(wn)

    @staticmethod
    def get_home_dir():
        return pwd.getpwuid(os.getuid()).pw_dir

    def main(self):
        return 0

    if __name__ == '__main__':
        main()
