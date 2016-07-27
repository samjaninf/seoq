import json
import requests
import urllib2
from django.conf import settings

# you can simplify a lot of this code using requests library! --jlariza


class JSONPrint(object):

    def makeRequest(self, url, keywords, depth, ip):
        if "http://" not in url:
            url = "http://" + url

        # makes request
        r = requests.post(settings.QSCRAPER_URL + '/api/seoq-tool/start-job/',
                          json={'url': url,
                                'keywords': keywords,
                                'depth': depth,
                                'ip': ip})
        data = r.json()
        job_id = data['job_id']  # gets job id

        # get status of the job
        getRequest = requests.get(
            settings.QSCRAPER_URL + '/api/status/' + job_id + '/').json()

        # continues to get the status of the job until it is finished
        # you should add a delay or you will make a request every few
        # miliseconds, giving the qscraper server a lot of pressure --jlariza
        while getRequest['status'] != 'finished':
            getRequest = json.load(
                urllib2.urlopen(
                    settings.QSCRAPER_URL + '/api/status/' + job_id + '/'))

        # gets request after the job is finished
        getRequest = json.load(
            urllib2.urlopen(
                settings.QSCRAPER_URL + '/api/seoq/' + job_id + '/'))
        # print getRequest['results'] #displays the results
        return getRequest


class QscraperSEOQTool(object):

    """
    class to organize all qscraper seotool related
    methods
    """
    def __init__(self, url, keywords, depth, ip):
        results = JSONPrint()
        self.url = url
        self.keywords = keywords
        self.depth = depth
        self.ip = ip
        self.JSONObject = (results.makeRequest(url, keywords, depth, ip))

    def calculate_headings(self):
        kwlength = len(self.keywords)
        headings = (self.JSONObject['results'])['headers']
        total_of_headers = headings['total_of_headers']  # number of headers
        # number of keywords in headers
        number_of_kws_in_headers = headings['number_of_kws_in_headers']
        score = number_of_kws_in_headers / float(
            total_of_headers * kwlength) * 10  # score
        return score

    def calc_tlinks(self):
        # get the url data
        links = (self.JSONObject['results'])['links_text']
        totalLinks = links['total_of_links_text']
        kwLinks = links['number_of_kws_in_links_text']
        # turn it into a score out of 10
        score = 10 * kwLinks / float(totalLinks * len(self.keywords))
        print score
        return score

    def calculate_title(self):
        titles = (self.JSONObject['results'])['page_title']
        # gets number of keywords in title
        kw_in_title = titles['number_of_kws_in_titles']
        # number of keywords
        kw_length = len(self.keywords)
        # calculates the score (1-10)
        score = kw_in_title / float(kw_length) * 10
        return score

    def calculate_url(self):
        # get the url data
        URLS = (self.JSONObject['results'])['urls']
        totalURLS = URLS['total_of_urls']
        kwURLS = URLS['number_of_kws_in_url']
        # turn it into a score out of 10
        score = 10 * kwURLS / float(totalURLS * len(self.keywords))
        print score
        return score

    def list_anchor_text(self):
        # get the url data
        extra_data = self.JSONObject['extra_data']
        links_data = extra_data['links_data']
        # list of unicode anchor text strings
        List_AnchorText = links_data['anchor_text']
        # creates a clean list that turns unicode string into regular string
        Clean_List = []
        for text in List_AnchorText:
            Clean_List.append(str(text))
        return Clean_List  # returns clean string

    def list_images(self):
        # get the url data
        extraData = self.JSONObject['extra_data']
        imagesData = extraData['images_data']
        # create a matrix that has every image, first column is the sources,
        # second column is the alt text, third column is the title

        # each row is the data for each picture
        Matrix = [[0 for x in range(3)] for y in range(len(imagesData['src']))]
        for count in range(len(imagesData['src'])):
            for item in imagesData['src']:
                Matrix[count][0] = item
            for item in imagesData['alt_text']:
                Matrix[count][1] = item
            for item in imagesData['title']:
                Matrix[count][2] = item
        return Matrix

    def get_meta_description(self):
        # get the url data
        metaDescription = self.JSONObject['results']
        metaDescription = metaDescription[
            'meta_description']['meta_description_content']
        Clean_List = ''
        for text in metaDescription:
            Clean_List = Clean_List + (str(text.encode('utf-8')))
        if len(Clean_List) > 160:
            Clean_List = Clean_List[:160] + '...'
        Clean_List = Clean_List.split(' ')
        print Clean_List
        return Clean_List

    def get_title(self):
        # get the url data
        title = self.JSONObject['extra_data']
        title = title['page_titles']
        Clean_List = ''
        for text in title:
            Clean_List = Clean_List + (str(text))
        if len(Clean_List) > 70:
            Clean_List = Clean_List[:70]
            if Clean_List.rfind(' ') != -1:
                Clean_List = Clean_List[:Clean_List.rfind(' ')] + '...'
            else:
                Clean_List = Clean_List + '...'
        return Clean_List

    def get_url(self, url):
        if len(url) > 70:
            url = url[:70] + '...'
        return url
