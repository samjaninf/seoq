import urllib
import json
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

        query = url[:url.find('.com')]
        key = 'AIzaSyCM6HT_sT9W7NHB-riLqxtYllvUU94Ys1k'

        MyUrl = ('https://maps.googleapis.com/maps/api/place/textsearch/json'
                 '?query=%s'
                 '&key=%s') % (query, key)

        # grabbing the JSON result
        response = urllib.urlopen(MyUrl)
        jsonRaw = response.read()
        jsonData = json.loads(jsonRaw)

        results = JSONPrint()
        JSONObject = (results.makeRequest(url, ["red"], 0, "72.194.193.110"))['extra_data']
        title = (str(JSONObject['page_titles'][0]))
        print title 

        for i in range(0, len(jsonData['results'])):
            name = jsonData['results'][i]['name'].lower().replace(' ', '')
            if query in name:
                return True    

        return False