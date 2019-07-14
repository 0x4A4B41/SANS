import objc
import os
import pwd

from ..Platform.Common import BSSID
from ..Platform.Common import WirelessNetwork

""" MacOS - platform specific code """


class MacOS():
    """ Initialization function """
    def __init__(self):
        pass

    # Scan Networks - scan for wireless networks
    # :return result object

    def scan_wifi(self):
        bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
        objc.loadBundle('CoreWLAN',
                        bundle_path=bundle_path,
                        module_globals=globals())

        iface = CWInterface.interface()
        results, errors = iface.scanForNetworksWithName_error_(None, None)

        wireless_nets = []

        for result in results:
            wnbssid = BSSID()
            wnbssid.set_bssid(str(result.bssid()))
            wnbssid.set_ssid(str(result.ssid()))
            wnbssid.set_channel(str(result.channel()))
            wn = WirelessNetwork(str(result.ssid()))
            wn.set_auth(result.securityMode())
            wn.set_bssid(wnbssid)
            wireless_nets.append(dict({
                'ssid': str(result.ssid()),
                'mac address': str(result.bssid()),
                'rssi': str(result.rssi()),
                'security': result.securityMode()
                                       }))
        return wireless_nets

    @staticmethod
    def get_home_dir():
        return pwd.getpwuid(os.getuid()).pw_dir

    def main(self):
        return 0

    if __name__ == '__main__':
        main()
