'''

'''

from urllib.request import urlopen
import urllib.request
import re
import ssl

class MacLookUpTableItem:

    # Init
    def __init__(self,macoui,shortname,longname):
        self.macoui = macoui
        self.shortname = shortname
        self.longname = longname

class MacLookup:

    # Initializer
    def __init__(self, macaddress):
        self.macaddress = macaddress
        self.lookupitemlist = []

    def retrieveOUITable (self):
        ssl._create_default_https_context = ssl._create_unverified_context
        ouitable = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"
        pattern = re.compile(".*00:50:56.*")
        for line in urlopen(ouitable):
            linesplit = str(line, 'utf-8').split("\t")
            if len(linesplit) == 3:
                thisouiinstance = MacLookUpTableItem (linesplit[0],linesplit[1],linesplit[2])
                self.lookupitemlist.append (thisouiinstance)
        print ("loaded items: " + str (len(self.lookupitemlist)))
    # def macLookup (self):
    #    pass

    def printOUIReference(self):
        for ptr in self.lookupitemlist:
            print ("--> " + ptr.macoui + ":" + ptr.longname)
'''
OUI 48 bits first - 24 always vendor.. netmask for remainder

'''
ml = MacLookup ("00:50:56:c0:00:08")
ml.retrieveOUITable()
ml.printOUIReference()


