import requests
from dns.resolver import Resolver

from CapstoneClient.WiFiScanner.WiFiScanner import WiFiScanner, security_mode

dns_prefix = 'http://192.168.65.24:5000'
dns_endpoint = '/dnscheck'
oui_prefix = 'http://192.168.65.24:5000'
oui_endpoint = '/macouilookup'


class ApiError(Exception):
    pass


class Main:

    def lookup_dns(self):
        r = Resolver()
        resultset = []
        topsites = ['google.com', 'facebook.com', 'apple.com', 'amazon.com']
        for topsite in topsites:
            answer = r.query(topsite, 'soa')
            for soa in answer.rrset.items:
                soa_split = str(soa).split(' ')
                serial = soa_split[2]
                resultset.append(dict({'domain': topsite, 'soa': str(soa), 'serial': serial}))
        return resultset

    def lookup_all_dns_from_service(self):
        json_list = []
        resp = requests.get(dns_prefix + dns_endpoint, None)
        if resp.status_code != 200:
            raise ApiError('GET {} {}'.format(dns_prefix, resp.status_code))
        for dns_item in resp.json():
            json_list.append(dns_item)
        return json_list

    def lookup_one_dns_from_service(self, json_package):
        json_list = []
        resp = requests.post(dns_prefix + dns_endpoint, None, json_package)
        if resp.status_code != 200:
            raise ApiError('POST {} {}'.format(dns_prefix, resp.status_code))
        for dns_item in resp.json():
            json_list.append(dns_item)
        return json_list

#######################
    def lookup_one_oui_from_service(self, json_package):
        json_list = []
        resp = requests.post(oui_prefix + oui_endpoint, None, json_package)
        if resp.status_code != 200:
            raise ApiError('POST {} {}'.format(oui_prefix, resp.status_code))
        for oui_item in resp.json():
            json_list.append(oui_item)
        return json_list

    def main(self):
        # scan for wireless networks and return only the ones that are not open nets
        _WiFiScanner = WiFiScanner()
        _WiFiNets = _WiFiScanner.scan()
        # lookup up the mac addresses of the nets returned to check manufacturer
        try:
            for net in _WiFiNets:
                loaded_net = {'oui': net['mac address'].upper()[0:8]}
                oui_lookup = self.lookup_one_oui_from_service(loaded_net)
                print(net['ssid'])
#                print("loaded_net: " + str(loaded_net))
                if _WiFiScanner.isMac:
                    print(" Security: " + security_mode[net['security']])
                elif _WiFiScanner.isWin:
                    print(" Security: " + net['security'])
                if oui_lookup is None:
                    print(' No Router info returned')
                else:
                    if len(oui_lookup) == 0:
                        print(" No router info returned")
                    for lookup in oui_lookup:
                        print(' Router info:' + lookup['longname'])
        except TypeError:
            print ("exception")
            pass

        """
        service_response = self.lookup_all_dns_from_service()
        internal_response = self.lookup_dns()
        for dns_item in service_response:
            match = False
            for inner_dns_item in internal_response:
                #TODO: subtract serial from SOA and compare
                if (str(dns_item['domain']) == str(inner_dns_item['domain'])):
                    if (str(dns_item['soa']) == str(inner_dns_item['soa']) and
                        str(dns_item['serial'] == str(inner_dns_item['serial']))):
                        match = True
                    if match:
                        print("MATCH______")
                        print('LOCAL: domain: {} soa: {} serial: {}'.format(inner_dns_item['domain'], inner_dns_item['soa'],
                                                                       inner_dns_item['serial']))
                        print('REST : domain: {} soa: {} serial: {}'.format(dns_item['domain'], dns_item['soa'],
                                                                            dns_item['serial']))
                        break
                    else:
                        print("NO MATCH__")
                        print('LOCAL: domain: {} soa: {} serial: {}'.format(inner_dns_item['domain'], inner_dns_item['soa'],
                                                                        inner_dns_item['serial']))
                        print('REST : domain: {} soa: {} serial: {}'.format(dns_item['domain'], dns_item['soa'],
                                                                            dns_item['serial']))
        """



if __name__ == '__main__':
    _Main = Main()
    _Main.main()