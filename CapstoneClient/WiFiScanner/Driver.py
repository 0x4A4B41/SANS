import sys
if sys.platform == "darwin":
    from CapstoneClient.WiFiScanner.MacOS import MacOS
elif sys.platform == "win32":
    from CapstoneClient.WiFiScanner.Win32 import Win32


class Driver:

    def __init__(self):
        if sys.platform == "darwin":
            self.isMac = True
            self.isWin = False
            self.isLin = False
        elif sys.platform == "win32":
            self.isMac = False
            self.isWin = True
            self.isLin = False

    """ Preliminary network scan - enumerate WireLess SSIDs and BSSIDs and do general recon
    """
    def pre_connect_scan(self):
        if self.isMac:
            platform_obj = MacOS()
        elif self.isWin:
            platform_obj = Win32()
        wifi_scan_results = platform_obj.scan_wifi()
        for net in wifi_scan_results:
          pass
        # print (wifi_scan_results)

    def main(self):
        self.pre_connect_scan()


if __name__ == '__main__':
    _Driver = Driver()
    _Driver.main()

'''

import objc
import json

bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
objc.loadBundle('CoreWLAN',
                bundle_path=bundle_path,
                module_globals=globals())

iface = CWInterface.interface()
result,errors = iface.scanForNetworksWithSSID_includeHidden_error_(None, True, None)
jdata = []

for r in result:
    print (r)

'''