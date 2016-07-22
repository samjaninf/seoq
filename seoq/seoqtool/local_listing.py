import urllib
import json
import string
from qscraper_utils import JSONPrint
from django.conf import settings


class LocalListing(object):

    def main(self, url):
        localListingExists = self.getLocalListing(url)
        print('Google local listing for ' + url + ' exists: ' + str(localListingExists))

    def getLocalListing(self, url):
        # formatting url
        if url.find('http://') != -1 or url.find('https://') != -1:
            url = url[url.find('/') + 2:]
        if url.find('www.') != -1:
            url = url[url.find('.') + 1:]

        query = url[:url.find('.')].lower()
        exclude = set(string.punctuation)
        query = ''.join(ch for ch in query if ch not in exclude)

        key = settings.GOOGLE_PLACES_API_KEY
        apiURL = str(settings.GOOGLE_PLACES_URL)

        MyUrl = (apiURL +
                 '?query=%s'
                 '&key=%s') % (query, key)

        # grabbing the JSON result
        response = urllib.urlopen(MyUrl)
        jsonRaw = response.read()
        jsonData = json.loads(jsonRaw)

        #results = JSONPrint()
        #JSONObject = results.makeRequest(url, ["red"], 0, "72.194.193.110")['extra_data']

        #title = (str(JSONObject['page_titles'][0])).lower().replace(' ', '')
        #title = ''.join(ch for ch in title if ch not in exclude)

        for i in range(len(jsonData['results'])):
            print jsonData['results'][i]['name']

        for i in range(len(jsonData['results'])):
            print(len(jsonData['results'])) 
            print query[0]
            print jsonData['results'][i]['name']
            if query[0] in jsonData['results'][i]['name'].lower():
                return True

        return False

        '''if len(jsonData['results']) > 0:
            return True
        else:
            return False'''

        '''for i in range(len(jsonData['results'])):
            name = jsonData['results'][i]['name'].lower().replace(' ', '')
            exclude = set(string.punctuation)
            name = ''.join(ch for ch in name if ch not in exclude)
            print('n' + name)
            if query in name:
                return True
            if title in name:
                return True'''

        return False