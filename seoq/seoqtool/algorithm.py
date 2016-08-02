import math
from .utils import get_built_with_information
from .utils import get_total_time_and_ssl_certification
from .majestic_utils import MajesticBackLinks
from .checker_utils import Checker_Utils
from .qscraper_utils import QscraperSEOQTool
from .local_listing import LocalListing
from .mobilefriendlycheck import MobileFriendlyChecker
# Create your views here.


class Algorithm(object):
    """
    Has algorithm for score.
    """
    backlinkVar = 1
    trustFlowVar = 1
    robotsVar = 1
    listingVar = 1
    keyVar = 1

    def __init__(self, netloc):
        self.netloc = str(netloc)
        self.majestic = MajesticBackLinks(netloc)
        self.checker = Checker_Utils()
        self.local = LocalListing()
        self.mobile = MobileFriendlyChecker()
        self.check_robots = self.checker.checkRobots(netloc)
        self.total_time_and_ssl = get_total_time_and_ssl_certification(netloc)
        self.cms = get_built_with_information(netloc).get('cms', [])

    def changeVar(self, backlinkVar, trustFlowVar,
                  robotsVar, listingVar, keyVar):
        self.backlinkVar = backlinkVar
        self.trustFlowVar = trustFlowVar
        self.robotsVar = robotsVar
        self.listingVar = listingVar
        self.keyVar = keyVar

    def getSiteScore(self):
        score = float(100)
        avgTime = float(0.150895375)

        if self.netloc.find('.gov') != -1:
            score = score + 6
        elif self.netloc.find('.edu') != -1:
            score = score + 3
        if self.total_time_and_ssl['ssl_certificate']:
            score = score + 5
        time = self.total_time_and_ssl['speed_info']
        time = float(time['time_in_seconds'])
        if time > 0:
            score = score + (float(time) / float(2 * avgTime) - .5) / -10
        if self.cms:
            score = score + 5
        backlinks = float(self.majestic.getNumBackLinksDomainName())
        if backlinks > 0:
            score = score + float(math.log(backlinks)) * self.backlinkVar
        backlinks = float(self.majestic.getNumBackLinksWebPageURL())
        if backlinks > 0:
            score = score + float(math.log(backlinks)) * self.backlinkVar
        govlinks = float(self.majestic.getNumGovBackLinksDomainName())
        if govlinks > 0:
            score = score + float(math.log(govlinks)) * self.backlinkVar / 2
        govlinks = float(self.majestic.getNumGovBackLinksWebPageURL())
        if govlinks > 0:
            score = score + float(math.log(govlinks)) * self.backlinkVar / 2
        edulinks = float(self.majestic.getNumEduBackLinksDomainName())
        if edulinks > 0:
            score = score + float(math.log(edulinks)) * self.backlinkVar / 3
        edulinks = float(self.majestic.getNumEduBackLinksWebPageURL())
        if edulinks > 0:
            score = score + float(math.log(edulinks)) * self.backlinkVar / 3
        trustFlow = float(self.majestic.getTrustFlow())
        if trustFlow > 0:
            score = score + trustFlow - self.trustFlowVar
        refIPS = float(self.majestic.getRefIPs())
        if refIPS > 0:
            score = score + float(math.log(refIPS))
        if self.check_robots[0].find('Robots allowed') != -1:
            score = score + self.robotsVar
        else:
            score = score - self.robotsVar * 3
        if self.check_robots[1].find('Sitemap found') != -1:
            score = score + self.robotsVar
        else:
            score = score - self.robotsVar * 2
        if self.local.main(self.netloc) == 'This listing does exist':
            score = score + self.listingVar
        else:
            score = score - self.listingVar
        if self.mobile.checkMobileFriendly(self.netloc) is True:
            score = score + self.listingVar
        else:
            score = score - self.listingVar
        return int(score)

    def getKeywordClass(self, url, keyword, ip=1223):
        self.scraper = QscraperSEOQTool(url, keyword, ip)

    def getKeywordScore(self, url, keyword):
        self.getKeywordClass(url, keyword)
        score = 100
        score = self.getSiteScore(url)
        score = score + (
            (self.scraper.calculate_headings() - 5) * self.keyVar / 2)
        score = score + (self.scraper.calc_tlinks() - 5) * self.keyVar / 3
        score = score + ((self.scraper.calculate_title() - 5) * self.keyVar)
        score = score + ((self.scraper.calculate_url() - 5) * self.keyVar)
        anchorLinks = self.majestic.getAnchorTextBackLinks(keyword)
        score = score + anchorLinks - 5
        return int(score)
