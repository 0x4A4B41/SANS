import sys
if sys.platform == "darwin":
    from CapstoneClient.WiFiScanner.MacOS import MacOS
elif sys.platform == "win32":
    from CapstoneClient.WiFiScanner.Win32 import Win32

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


class WiFiScanner:

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
    def scan(self):
        if self.isMac:
            platform_obj = MacOS()
        elif self.isWin:
            platform_obj = Win32()
        nets = platform_obj.scan_wifi()
        for net in nets:
            if isinstance(net['security'], int):
                if net['security'] == 0: #remove open networks from further analysis - insecure
                    nets.remove(net)
            elif isinstance(net['security'], str):
                if net['security'].lower().replace(" ", "") == 'open':
                    nets.remove(net)
        return nets
