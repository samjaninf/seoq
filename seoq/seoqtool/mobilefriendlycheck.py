# 19 July 2016, Jessie Shen
# Returns if given website input passes google mobile-friendly test.


import requests


class MobileFriendlyChecker(object):

    def checkMobileFriendly(self, site):
        url = site
        if url.find('http://') == -1 & url.find('https://') == -1:
            url = 'http://' + url
        params = {
            'key': 'AIzaSyDkEX-f1JNLQLC164SZaobALqFv4PHV-kA',
            'url': url,
        }
        api_url = 'https://www.googleapis.com/pagespeedonline/v3beta1/mobileReady'
        response = requests.get(api_url, params=params)
        data = response.json()
        try:
            answer = data['ruleGroups']['USABILITY']['pass']
            return answer
        except:
            return "Looks like the API is down."

mfcobj = MobileFriendlyChecker()
url = raw_input('Enter your url to test: ')
ans = mfcobj.checkMobileFriendly(url)
print ans
