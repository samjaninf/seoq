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
    score = 0

    def getSiteScore(self, netloc):
        netloc = str(netloc)
        majestic = MajesticBackLinks()
        checker = Checker_Utils()
        local = LocalListing()
        mobile = MobileFriendlyChecker()
        score = float(100)
        avgTime = float(0.150895375)
        total_time_and_ssl = get_total_time_and_ssl_certification(netloc)
        check_robots = checker.checkRobots(netloc)

        if netloc.find('.gov') != -1:
            score = score + 6
        elif netloc.find('.edu') != -1:
            score = score + 3
        if total_time_and_ssl['ssl_certificate']:
            score = score + 5
        time = total_time_and_ssl['speed_info']
        time = float(time['time_in_seconds'])
        if time > 0:
            score = score + (float(time) / float(2 * avgTime) - .5) / -10
        if get_built_with_information(netloc).get('cms', []):
            score = score + 5
        backlinks = float(majestic.getNumBackLinksDomainName(netloc))
        if backlinks > 0:
            score = score + float(math.log(backlinks)) * 2
        backlinks = float(majestic.getNumBackLinksWebPageURL(netloc))
        if backlinks > 0:
            score = score + float(math.log(backlinks)) * 2
        govlinks = float(majestic.getNumGovBackLinksDomainName(netloc))
        if govlinks > 0:
            score = score + float(math.log(govlinks))
        govlinks = float(majestic.getNumGovBackLinksWebPageURL(netloc))
        if govlinks > 0:
            score = score + float(math.log(govlinks))
        edulinks = float(majestic.getNumEduBackLinksDomainName(netloc))
        if edulinks > 0:
            score = score + float(math.log(edulinks))
        edulinks = float(majestic.getNumEduBackLinksWebPageURL(netloc))
        if edulinks > 0:
            score = score + float(math.log(edulinks))
        trustFlow = float(majestic.getTrustFlow(netloc))
        if trustFlow > 0:
            score = score + trustFlow - 5
        refIPS = float(majestic.getRefIPs(netloc))
        if refIPS > 0:
            score = score + float(math.log(refIPS))
        if check_robots[0].find('Robots allowed') != -1:
            score = score + 5
        else:
            score = score - 15
        if check_robots[1].find('Sitemap found') != -1:
            score = score + 5
        else:
            score = score - 10
        if local.main(netloc) == 'This listing does exist':
            score = score + 5
        else:
            score = score - 5
        if mobile.checkMobileFriendly(netloc) is True:
            score = score + 5
        else:
            score = score - 5
        return int(score)

    def getKeywordScore(self, url, keyword, ip=1223):
        scraper = QscraperSEOQTool(url, keyword, 0, ip)
        majestic = MajesticBackLinks()
        score = 100
        score = self.getSiteScore(url)
        score = score + ((scraper.calculate_headings() - 5) * 2)
        score = score + (scraper.calc_tlinks() - 5)
        score = score + ((scraper.calculate_title() - 5) * 3)
        score = score + ((scraper.calculate_url() - 5) * 3)
        anchorLinks = majestic.getAnchorTextBackLinks(
            url, keyword)
        score = score + anchorLinks - 5
        return int(score)
