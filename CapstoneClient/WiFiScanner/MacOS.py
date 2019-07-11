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


    """ Scan Networks - scan for wireless networks
    :return result object """
    def scan_wifi(self):
        bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
        objc.loadBundle('CoreWLAN',
                        bundle_path=bundle_path,
                        module_globals=globals())
        iface = CWInterface.interface()
        results, errors = iface.scanForNetworksWithName_includeHidden_error_(None, True, None)
        security_mode = [
            'Open',                  #0
            'WEP',                   #1
            'WPAPersonal'            #2
            'WPAPersonalMixed',      #3
            'WPA2Personal',          #4
            'Personal',              #5
            'Dynamic WEP',           #6
            'WPA Enterprise',        #7
            'WPA EnterpriseMixed'    #8
            'WPA2 Enterprise'        #9
            'Enterprise'             #10
        ]
        wireless_nets = []
        for result in results:
            print(result)
            wnbssid = BSSID()
            wnbssid.set_bssid(str(result.bssid()))
            wnbssid.set_ssid(str(result.ssid()))
            wnbssid.set_channel(str(result.channel()))
            wn = WirelessNetwork(str(result.ssid()))
            wn.set_auth(str(security_mode[result.securityMode()]))
            wn.set_bssid(wnbssid)

            security_mode = [
                'Open',  # 0
                'WEP',  # 1
                'WPAPersonal'  # 2
                'WPAPersonalMixed',  # 3
                'WPA2Personal',  # 4
                'Personal',  # 5
                'Dynamic WEP',  # 6
                'WPA Enterprise',  # 7
                'WPA EnterpriseMixed'  # 8
                'WPA2 Enterprise'  # 9
                'Enterprise'  # 10
            ]

            wireless_nets.append(dict({
                'ssid': str(result.ssid()),
                'mac address': str(result.bssid()),
                'rssi': str(result.rssi()),
                'security': str(security_mode[result.securityMode()])
                                       }))
            return wireless_nets

    @staticmethod
    def get_home_dir():
        return pwd.getpwuid(os.getuid()).pw_dir

    def main(self):
        return 0

    if __name__ == '__main__':
        main()
