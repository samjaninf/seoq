# import API service
from majesticseo_external_rpc.APIService import APIService
from django.conf import settings


class MajesticBackLinks(object):

    def main(self, url):
        # replace it for a method variable
        # in order to allow other urls
        # --jlariza

        numGovBackLinksWebPageURL = self.getNumGovBackLinksWebPageURL(url)
        print('Number of Gov External Backlinks for page URL of ' +
              url + ': ' + numGovBackLinksWebPageURL)

        numGovBackLinksDomainName = self.getNumGovBackLinksDomainName(url)
        print('Number of Gov External Backlinks for domain name of ' +
              url + ': ' + numGovBackLinksDomainName)

        numEduBackLinksWebPageURL = self.getNumEduBackLinksWebPageURL(url)
        print('Number of Edu External Backlinks for page URL of ' +
              url + ': ' + numEduBackLinksWebPageURL)

        numEduBackLinksDomainName = self.getNumEduBackLinksDomainName(url)
        print('Number of Edu External Backlinks for domain name of ' +
              url + ': ' + numEduBackLinksDomainName)

    def getNumBackLinksDomainName(self, url):
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
                # print('Number of External Backlinks for ' + str(item) +
                #       ': ' + row.get('ExtBackLinks'))
                numBackLinks = row.get('ExtBackLinks')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumBackLinksWebPageURL(self, url):
        # removed the hardcoded information
        # --jlariza

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
                # print('Number of External Backlinks for ' + str(item) +
                #       ': ' + row.get('ExtBackLinks'))
                numBackLinks = row.get('ExtBackLinks')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumGovBackLinksDomainName(self, url):
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
                # print('Number of External Backlinks for ' + str(item) +
                #       ': ' + row.get('ExtBackLinks'))
                numBackLinks = row.get('ExtBackLinksGOV')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumGovBackLinksWebPageURL(self, url):
        # removed the hardcoded information
        # --jlariza

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
                # print('Number of External Backlinks for ' + str(item) +
                #       ': ' + row.get('ExtBackLinks'))
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
                # print('Number of External Backlinks for ' + str(item) +
                #       ': ' + row.get('ExtBackLinks'))
                numBackLinks = row.get('ExtBackLinksEDU')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

    def getNumEduBackLinksWebPageURL(self, url):
        # removed the hardcoded information
        # --jlariza

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
                # print('Number of External Backlinks for ' + str(item) +
                #       ': ' + row.get('ExtBackLinks'))
                numBackLinks = row.get('ExtBackLinksEDU')
            return numBackLinks

        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))
