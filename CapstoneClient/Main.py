from dns.resolver import Resolver
import requests

dns_prefix = 'http://localhost:5000'
dns_endpoint = '/dnscheck'



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

    def main(self):
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




if __name__ == '__main__':
    _Main = Main()
    _Main.main()