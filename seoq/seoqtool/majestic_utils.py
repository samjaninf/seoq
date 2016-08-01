# import API service
from majesticseo_external_rpc.APIService import APIService
from django.conf import settings


class MajesticBackLinks(object):

    def __init__(self, url):
        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        domainURL = url
        if url.find('http://') != -1 or url.find('https://') != -1:
            domainURL = url[url.find('/') + 2:]
        if url.find('www.') != -1:
            domainURL = url[url.find('.') + 1:]
        if url.find('/') != -1:
            domainURL = url[:url.find('/')]
        items = [domainURL]
        item_to_query = domainURL

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)

        self.indexItemInfoDomainNameResponse = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        # if url has https:// in it, then replace it
        #               with http:// for further analysis

        pageURL = url
        if url.find('https://') != -1:
            pageURL = url.replace('https://', 'http://')

        # if already in format http://www.example.com
        if (url.find('www.') != -1) & (url.find('http://') != -1):
            pageURL = url
        # if in format www.example.com
        elif (url.find('www.') != -1) & (url.find('http://') == -1):
            pageURL = 'http://' + url
        # if in format example.com
        elif (url.find('www.') == -1) & (url.find('http://') == -1):
            pageURL = 'http://www.' + url
        # if in format http://example.com
        elif (url.find('www.') == -1) & (url.find('http://') != -1):
            pageURL = url.replace('http://', 'http://www.')
        items = [pageURL]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        self.indexItemInfoWebPageURLResponse = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # for getting response for backlink data
        parameters = {}
        parameters['Count'] = '50000'
        parameters['item'] = item_to_query
        parameters['Mode'] = '0'
        parameters['datasource'] = 'fresh'

        self.backLinkDataReponse = api_service.execute_command(
            'GetBackLinkData', parameters)

    def main(self, url, keywords):

        print('BackLinks Domain: ' + str(self.getNumBackLinksDomainName()))
        print('BackLinks URL: ' + str(self.getNumBackLinksWebPageURL()))
        print('BackLinks Gov Domain: ' + str(self.getNumGovBackLinksDomainName()))
        print('Backlinks Gov URL: ' + str(self.getNumGovBackLinksWebPageURL()))
        print('Backlinks Edu Domain: ' + str(self.getNumEduBackLinksDomainName()))
        print('Backlinks Edu URL: ' + str(self.getNumEduBackLinksWebPageURL()))
        print('Ref IPs: ' + str(self.getRefIPs()))
        print('Trust Flow: ' + str(self.getTrustFlow()))
        print('Anchor Text BackLinks: ' +
              str(self.getAnchorTextBackLinks(keywords)))
        print('Citation Flow Backlinks: ' +
              str(self.getCitationFlowBackLinks()))

    def getNumBackLinksDomainName(self):
        response = self.indexItemInfoDomainNameResponse

        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                numBackLinks = row.get('ExtBackLinks')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumBackLinksWebPageURL(self):
        response = self.indexItemInfoWebPageURLResponse
        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                numBackLinks = row.get('ExtBackLinks')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumGovBackLinksDomainName(self):
        response = self.indexItemInfoDomainNameResponse

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                numBackLinks = row.get('ExtBackLinksGOV')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumGovBackLinksWebPageURL(self):
        response = self.indexItemInfoWebPageURLResponse

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                numBackLinks = row.get('ExtBackLinksGOV')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumEduBackLinksDomainName(self):
        response = self.indexItemInfoDomainNameResponse

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                numBackLinks = row.get('ExtBackLinksEDU')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumEduBackLinksWebPageURL(self):
        response = self.indexItemInfoWebPageURLResponse

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                numBackLinks = row.get('ExtBackLinksEDU')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getTrustFlow(self):
        response = self.indexItemInfoDomainNameResponse

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                trustFlow = row.get('TrustFlow')
            return float(trustFlow) / 10

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getRefIPs(self):
        response = self.indexItemInfoDomainNameResponse

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                refIPs = row.get('RefIPs')
            return refIPs

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getAnchorTextBackLinks(self, keywords):
        response = self.backLinkDataReponse

        # check the response code
        if(response.is_ok()):
            # print the URL table
            numKeyWordsInAnchorText = 0
            results = response.get_table_for_name('BackLinks')
            for row in results.rows:
                for word in keywords:
                    if row['AnchorText'].find(word) != -1:
                        numKeyWordsInAnchorText += 1
            return float(numKeyWordsInAnchorText) / float(len(results.rows)) * 10

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getCitationFlowBackLinks(self):
        response = self.backLinkDataReponse

        # check the response code
        if(response.is_ok()):
            # print the URL table
            results = response.get_table_for_name('BackLinks')
            totalCitationFlow = 0
            for row in results.rows:
                totalCitationFlow += int(row.get('SourceCitationFlow'))
            return float(totalCitationFlow) / (float(len(results.rows)) * 10)

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))
