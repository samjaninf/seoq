# 7.18.16 Kunal Naik
# The purpose of this file is to see if robots can crawl the site
# Second purpose is to find the sitemap

import requests
from django.utils.html import strip_tags


class Checker_Utils(object):
    # needs plain domain such as 'http://www.espn.com'
    # returns (boolean of if robots are crawlable, boolean
    # if there is a sitemap)
    def checkRobots(self, url):
        siteResult = ''
        robotResult = ''

        # # if already in format http://www.example.com
        # if (url.find('www.') != -1) & (url.find('http://') != -1):
        #     url = url
        # # if in format www.example.com
        # elif (url.find('www.') != -1) & (url.find('http://') == -1):
        #     url = 'http://' + url
        # # if in format example.com
        # elif (url.find('www.') == -1) & (url.find('http://') == -1):
        #     url = 'http://www.' + url
        # # if in format http://example.com
        # elif (url.find('www.') == -1) & (url.find('http://') != -1):
        #     url = url.replace('http://', 'http://www.')
        # # add robots.txt standard
        url = url.replace(
            'www.', '').replace(
            'https://', 'http://')
        if 'http://' not in url:
            url = 'http://' + url
        response = requests.get(url)
        if response.text.find('<meta name="robots" content="noindex">') != -1:
            robotResult = 'Robots cannot crawl this page'
            return (robotResult, self.checkSitemap(url))
        # see if the robots file exists
        urlRobots = url + '/robots.txt'
        try:
            response = requests.get(urlRobots)
            if response.status_code != 200:
                return ('No robots.txt', self.checkSitemap(url))
        except requests.exceptions.RequestException:
            return ('No robots.txt', self.checkSitemap(url))

        response = requests.get(urlRobots)
        rText = strip_tags(response.text.encode('utf-8'))
        text_array = []
        # find all the lines in the robots.txt
        while rText.find("\n") != -1:
            text_array.append(str(rText[:rText.find("\n")]))
            rText = rText[rText.find("\n") + 1:]
        # find if there is a sitemap and if user-agent: * (robots can crawl)
        for item in text_array:
            if item[:7] == 'Sitemap':
                siteResult = 'Sitemap found'
            elif item[:10] == 'User-agent':
                robotResult = 'Robots allowed'
            elif item[:8] == 'Disallow':
                if len(robotResult) < 15:
                    robotResult = robotResult + ', some disallows'
        # if sitemap is not in robots.txt
        if len(siteResult) < 1:
            siteResult = self.checkSitemap(url)
        result = (robotResult, siteResult)
        return result

    # this method is for when there is no robots.txt
    def checkSitemap(self, url):
        # check sitemap sitemap.xml sitemap.txt
        # sitemap.html sitemap.htm sitemap.asp
        sitemap = ['/sitemap', '/sitemap.xml', '/sitemap.txt', '/sitemap.php',
                   '/sitemap.asp', '/sitemap.htm', '/sitemap.html']
        # search for 'sitemap' but exclude instances of exact url extension
        # such as sitemap.txt
        for item in sitemap:
            urlAdd = url + item
            try:
                r = requests.get(urlAdd)
                if r.text == '':
                    pass
                else:
                    index = r.text.find('sitemap')
                    if index == r.text.find(item):
                        pass
                    elif index != -1:
                        return 'Sitemap found'
                urlAdd = url
            except requests.exceptions.RequestException:
                pass
        return 'Sitemap not found'
