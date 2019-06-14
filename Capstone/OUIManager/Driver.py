import sys
if sys.platform == "darwin":
    from ..Platform.MacOS import MacOS
elif sys.platform == "win32":
    from ..Platform.Win32 import Win32


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

    """
    OUI logic: initial revision
    - check for existence of JSON file with OUI data 
    - if found - read it
    - if not found try downloading it
    - once downloaded - read it
    --- need consistent logic for how file is read 
    """
