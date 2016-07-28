# import API service
from majesticseo_external_rpc.APIService import APIService
from django.conf import settings


class MajesticBackLinks(object):

    def main(self, url, keywords):

        print('Ref IPs: ' + self.getRefIPs(url))
        print('Trust Flow: ' + self.getTrustFlow(url))
        print('Anchor Text BackLinks: ' +
              str(self.getAnchorTextBackLinks(url, keywords)))

    def getNumBackLinksDomainName(self, url):

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        if url.find('http://') != -1 or url.find('https://') != -1:
            url = url[url.find('/') + 2:]
        if url.find('www.') != -1:
            url = url[url.find('.') + 1:]
        if url.find('/') != -1:
            url = url[:url.find('/')]
        items = [url]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                item = row['Item']  # website you are analyzing
                numBackLinks = row.get('ExtBackLinks')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumBackLinksWebPageURL(self, url):

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        # if url has https:// in it, then replace it
        #               with http:// for further analysis

        if url.find('https://') != -1:
            url = url.replace('https://', 'http://')

        # if already in format http://www.example.com
        if (url.find('www.') != -1) & (url.find('http://') != -1):
            url = url
        # if in format www.example.com
        elif (url.find('www.') != -1) & (url.find('http://') == -1):
            url = 'http://' + url
        # if in format example.com
        elif (url.find('www.') == -1) & (url.find('http://') == -1):
            url = 'http://www.' + url
        # if in format http://example.com
        elif (url.find('www.') == -1) & (url.find('http://') != -1):
            url = url.replace('http://', 'http://www.')
        items = [url]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                item = row['Item']  # website you are analyzing
                numBackLinks = row.get('ExtBackLinks')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumGovBackLinksDomainName(self, url):

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        if url.find('http://') != -1 or url.find('https://') != -1:
            url = url[url.find('/') + 2:]
        if url.find('www.') != -1:
            url = url[url.find('.') + 1:]
        if url.find('/') != -1:
            url = url[:url.find('/')]
        items = [url]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                item = row['Item']  # website you are analyzing
                numBackLinks = row.get('ExtBackLinksGOV')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumGovBackLinksWebPageURL(self, url):

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        if url.find('https://') != -1:
            url = url.replace('https://', 'http://')

        # if already in format http://www.example.com
        if (url.find('www.') != -1) & (url.find('http://') != -1):
            url = url
        # if in format www.example.com
        elif (url.find('www.') != -1) & (url.find('http://') == -1):
            url = 'http://' + url
        # if in format example.com
        elif (url.find('www.') == -1) & (url.find('http://') == -1):
            url = 'http://www.' + url
        # if in format http://example.com
        elif (url.find('www.') == -1) & (url.find('http://') != -1):
            url = url.replace('http://', 'http://www.')
        items = [url]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                item = row['Item']  # website you are analyzing
                numBackLinks = row.get('ExtBackLinksGOV')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumEduBackLinksDomainName(self, url):
        # removed the hardcoded information
        # --jlariza

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        if url.find('http://') != -1 or url.find('https://') != -1:
            url = url[url.find('/') + 2:]
        if url.find('www.') != -1:
            url = url[url.find('.') + 1:]
        if url.find('/') != -1:
            url = url[:url.find('/')]
        items = [url]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                item = row['Item']  # website you are analyzing
                numBackLinks = row.get('ExtBackLinksEDU')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumEduBackLinksWebPageURL(self, url):

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        if url.find('https://') != -1:
            url = url.replace('https://', 'http://')

        # if already in format http://www.example.com
        if (url.find('www.') != -1) & (url.find('http://') != -1):
            url = url
        # if in format www.example.com
        elif (url.find('www.') != -1) & (url.find('http://') == -1):
            url = 'http://' + url
        # if in format example.com
        elif (url.find('www.') == -1) & (url.find('http://') == -1):
            url = 'http://www.' + url
        # if in format http://example.com
        elif (url.find('www.') == -1) & (url.find('http://') != -1):
            url = url.replace('http://', 'http://www.')
        items = [url]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                item = row['Item']  # website you are analyzing
                numBackLinks = row.get('ExtBackLinksEDU')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getTrustFlow(self, url):

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        if url.find('https://') != -1:
            url = url.replace('https://', 'http://')

        # if already in format http://www.example.com
        if (url.find('www.') != -1) & (url.find('http://') != -1):
            url = url
        # if in format www.example.com
        elif (url.find('www.') != -1) & (url.find('http://') == -1):
            url = 'http://' + url
        # if in format example.com
        elif (url.find('www.') == -1) & (url.find('http://') == -1):
            url = 'http://www.' + url
        # if in format http://example.com
        elif (url.find('www.') == -1) & (url.find('http://') != -1):
            url = url.replace('http://', 'http://www.')
        items = [url]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                item = row['Item']  # website you are analyzing
                trustFlow = row.get('TrustFlow')
            return trustFlow

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getRefIPs(self, url):

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        # website to analyze; domain name must follow format of example.com,
        # web page URL must follow format of http://example.com

        if url.find('https://') != -1:
            url = url.replace('https://', 'http://')

        # if already in format http://www.example.com
        if (url.find('www.') != -1) & (url.find('http://') != -1):
            url = url
        # if in format www.example.com
        elif (url.find('www.') != -1) & (url.find('http://') == -1):
            url = 'http://' + url
        # if in format example.com
        elif (url.find('www.') == -1) & (url.find('http://') == -1):
            url = 'http://www.' + url
        # if in format http://example.com
        elif (url.find('www.') == -1) & (url.find('http://') != -1):
            url = url.replace('http://', 'http://www.')
        items = [url]

        # create a hash from the resulting array with the key being
        # 'item0 => first item to query, item1 => second item to query' etc
        parameters = {}
        for index, item in enumerate(items):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command(
            'GetIndexItemInfo', parameters)  # gets XML response

        # check the response code
        if(response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            for row in results.rows:
                item = row['Item']  # website you are analyzing
                refIPs = row.get('RefIPs')
            return refIPs

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getAnchorTextBackLinks(self, url, keywords):

        endpoint = settings.MAJESTIC_URL  # API
        app_api_key = settings.MAJESTIC_API_KEY  # put API key

        if url.find('http://') != -1 or url.find('https://') != -1:
            url = url[url.find('/') + 2:]
        if url.find('www.') != -1:
            url = url[url.find('.') + 1:]
        if url.find('/') != -1:
            url = url[:url.find('/')]
        item_to_query = url

        # set up parameters
        parameters = {}
        parameters['Count'] = '50000'
        parameters['item'] = item_to_query
        parameters['Mode'] = '0'
        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command('GetBackLinkData', parameters)

        # check the response code
        if(response.is_ok()):
            # print the URL table
            numKeyWordsInAnchorText = 0
            results = response.get_table_for_name('BackLinks')
            print(len(results.rows))
            for row in results.rows:
                for word in keywords:
                    if row['AnchorText'].find(word) != -1:
                        numKeyWordsInAnchorText += 1
            return float(numKeyWordsInAnchorText) / float(len(results.rows))
        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))
