import requests
import hashlib

'''
Code for detecting Captive Portal. Based on 
https://success.tanaza.com/s/article/How-Automatic-Detection-of-Captive-Portal-works
TODO: Check for SSL Certificate in consistency also
'''

class Captive_Portal:

    def __init__(self):
        self.hash = hashlib.sha256()

    '''
    Checks URL against hash of content
    :params url (String), hash (String)
    :return bool (True if response code isnt 200 or returns 0 length or if hash is bad
    '''
    def check_portal(self, url, hash):
        r = requests.get(url)
        self.hash.update(str(r.text).encode())
        if r.status_code != 200 or len(r.text) == 0:
            return True
        if self.hash.hexdigest() != hash:
            return True
        return False

    '''
    Checks against known URLs
    :return True for captured portal found | False for alternate
    '''
    def check_known_sites(self):
        is_captive = []
        captive_check_url = [
            {'platform': 'android', 'url': 'https://clients3.google.com',
             'digest': '5e135d05bf06324e13f4aac60d3559c24c4a90ec0cbccb71bb3e1fe298144636'
             },
            {'platform': 'ios', 'url': 'https://captive.apple.com',
             'digest': 'c1f49fca2bdca6c21fa714d7f3cfddc8bb5f310cf255e2df20a4b6f2d5730ca8'
             }
        ]
        for url in captive_check_url:
            if self.check_portal(url['url'], url['digest']):
                is_captive.append(False)
            else:
                is_captive.append(True)
        for is_cap in is_captive:
            if is_cap:
                return True

        return False

    def main (self):
        return self.check_known_sites()

if __name__ == '__main__':
    _Main = Captive_Portal()
    _Main.main()
