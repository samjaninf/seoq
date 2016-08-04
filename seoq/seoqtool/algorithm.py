#Kunal Naik 8.2.16
#The purpose of this file is to run the algorithm and get the SEOQ score with and without keyword

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
    backlinkVar = 2.0140845
    trustFlowVar = 2.0140845
    robotsVar = 5.5211267
    listingVar = 4.0422535
    keyVar = 1.521126761

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
        report = {
            'crawlability': {},
            'credibility': {},
            'conversation': {},
            'competition': {},
            'conversion': {}
        }
        if self.netloc.find('.gov') != -1:
            score = score + 6
        elif self.netloc.find('.edu') != -1:
            score = score + 3
        if self.total_time_and_ssl['ssl_certificate']:
            score = score + 5
            report['credibility']['https'] = 'passed'
        else:
            report['credibility']['https'] = 'error'

        time = self.total_time_and_ssl['speed_info']
        time = float(time['time_in_seconds'])
        print time
        if time > 0 and time <= avgTime:
            report['crawlability']['speed'] = 'passed'
        else:
            report['crawlability']['speed'] = 'to improve'

        if time > 0:
            score = score + (float(time) / float(2 * avgTime) - .5) / -10
        if self.cms:
            score = score + 5

        backlinks = float(self.majestic.getNumBackLinksDomainName())
        if backlinks > 0:
            backlinks = float(math.log(float(self.majestic.getNumBackLinksDomainName())))
            if backlinks > 12:
                backlinks = 12
                score = score + backlinks * self.backlinkVar
                if backlinks > 10:
                    report['credibility']['backlinks_domain'] = 'passed'
                else:
                    report['credibility']['backlinks_domain'] = 'to improve'
        else:
                report['credibility']['backlinks_domain'] = 'to improve'

        backlinks = float(self.majestic.getNumBackLinksWebPageURL())
        if backlinks > 0:
            backlinks = float(math.log(float(self.majestic.getNumBackLinksWebPageURL())))
            if backlinks > 12:
                backlinks = 12
                score = score + backlinks * self.backlinkVar
                if backlinks > 10:
                    report['credibility']['backlinks_url'] = 'passed'
                else:
                    report['credibility']['backlinks_url'] = 'to improve'
        else:
                report['credibility']['backlinks_url'] = 'to improve'

        govlinks = float(self.majestic.getNumGovBackLinksDomainName())
        if govlinks > 0:
            govlinks = float(math.log(float(self.majestic.getNumGovBackLinksDomainName())))
            if govlinks > 12:
                govlinks = 12
                score = score + govlinks * self.backlinkVar / 2
                if govlinks > 5:
                    report['credibility']['govlinks_domain'] = 'passed'
                else:
                    report['credibility']['govlinks_domain'] = 'to improve'
        else:
                report['credibility']['govlinks_domain'] = 'to improve'

        govlinks = float(self.majestic.getNumGovBackLinksWebPageURL())
        if govlinks > 0:
            govlinks = float(math.log(float(self.majestic.getNumGovBackLinksWebPageURL())))
            if govlinks > 12:
                govlinks = 12
                score = score + govlinks * self.backlinkVar / 2
                if govlinks > 5:
                    report['credibility']['govlinks_url'] = 'passed'
                else:
                    report['credibility']['govlinks_url'] = 'to improve'
        else:
                report['credibility']['govlinks_url'] = 'to improve'

        edulinks = float(self.majestic.getNumEduBackLinksDomainName())
        if edulinks > 0:
            edulinks = float(math.log(float(self.majestic.getNumEduBackLinksDomainName())))
            if edulinks > 12:
                edulinks = 12
                score = score + edulinks * self.backlinkVar / 3
                if edulinks > 5:
                    report['credibility']['edulinks_domain'] = 'passed'
                else:
                    report['credibility']['edulinks_domain'] = 'to improve'
        else:
                report['credibility']['edulinks_domain'] = 'to improve'

        edulinks = float(self.majestic.getNumEduBackLinksWebPageURL())
        if edulinks > 0:
            edulinks = float(math.log(float(self.majestic.getNumEduBackLinksWebPageURL())))
            if edulinks > 12:
                edulinks = 12
                score = score + edulinks * self.backlinkVar / 3
                if edulinks > 5:
                    report['credibility']['edulinks_url'] = 'passed'
                else:
                    report['credibility']['edulinks_url'] = 'to improve'
        else:
                report['credibility']['edulinks_url'] = 'to improve'

        trustFlow = float(self.majestic.getTrustFlow())
        if trustFlow > 0:
            score = score + trustFlow - self.trustFlowVar
            if trustFlow > 5:
                report['credibility']['trustflow'] = 'passed'
            else:
                report['credibility']['trustflow'] = 'to improve'
        else:
            report['credibility']['trustflow'] = 'to improve'

        refIPS = float(self.majestic.getRefIPs())
        if refIPS > 0:
            score = score + float(math.log(refIPS))
            if float(math.log(refIPS)) > 5:
                report['credibility']['edulinks_url'] = 'passed'
            else:
                report['credibility']['edulinks_url'] = 'to improve'
        else:
                report['credibility']['edulinks_url'] = 'to improve'

        if self.check_robots[0].find('Robots allowed') != -1:
            score = score + self.robotsVar
            report['crawlability']['robots'] = 'passed'
        else:
            score = score - self.robotsVar * 3
            report['crawlability']['robots'] = 'error'
        if self.check_robots[1].find('Sitemap found') != -1:
            score = score + self.robotsVar
            report['crawlability']['sitemap'] = 'passed'
        else:
            score = score - self.robotsVar * 2
            report['crawlability']['sitemap'] = 'error'
        if self.local.main(self.netloc) == 'This listing does exist':
            score = score + self.listingVar
            report['conversion']['google_listing'] = 'passed'
        else:
            score = score - self.listingVar
            report['conversion']['google_listing'] = 'error'
        if self.mobile.checkMobileFriendly(self.netloc) is True:
            score = score + self.listingVar
        else:
            score = score - self.listingVar
        return int(score), report

    def getKeywordClass(self, url, keyword, ip=1223):
        self.scraper = QscraperSEOQTool(url, keyword, ip)

    def getKeywordScore(self, url, keyword):
        self.getKeywordClass(url, keyword)
        report = {
            'content': {},
            'code': {},
        }
        url_score = self.scraper.calculate_url()
        title_score = self.scraper.calculate_title()
        tlinks_score = self.scraper.calc_tlinks()
        headings_score = self.scraper.calculate_headings()
        meta_description_score = self.scraper.calculate_meta_description()
        anchorLinks = self.majestic.getAnchorTextBackLinks(keyword)

        if title_score == 0:
            report['content']['kw_in_title'] = 'error'
        elif title_score < 5:
            report['content']['kw_in_title'] = 'to improve'
        else:
            report['content']['kw_in_title'] = 'passed'

        if headings_score == 0:
            report['content']['kw_in_headers'] = 'error'
        elif headings_score < 5:
            report['content']['kw_in_headers'] = 'to improve'
        else:
            report['content']['kw_in_headers'] = 'passed'

        if tlinks_score == 0:
            report['content']['kw_in_tlinks'] = 'error'
        elif tlinks_score < 5:
            report['content']['kw_in_tlinks'] = 'to improve'
        else:
            report['content']['kw_in_tlinks'] = 'passed'

        if anchorLinks == 0:
            report['content']['kw_in_anchor_links'] = 'error'
        elif anchorLinks < 5:
            report['content']['kw_in_anchor_links'] = 'to improve'
        else:
            report['content']['kw_in_anchor_links'] = 'passed'

        if not self.cms:
            report['content']['cms'] = 'passed'
        elif 'WordPress' in self.cms:
            report['content']['cms'] = 'passed'
        elif 'Drupal' in self.cms or 'Joomla' in self.cms:
            report['content']['cms'] = 'to improve'
        else:
            report['content']['cms'] = 'error'

        if url_score < 3:
            report['code']['kw_in_url'] = 'error'
        elif url_score < 7:
            report['code']['kw_in_url'] = 'to improve'
        else:
            report['code']['kw_in_url'] = 'passed'

        if meta_description_score < 3:
            report['code']['kw_in_meta_description'] = 'error'
        elif meta_description_score < 7:
            report['code']['kw_in_meta_description'] = 'to improve'
        else:
            report['code']['kw_in_meta_description'] = 'passed'

        score = 100
        # score = self.getSiteScore(url)
        score = score + (
            (headings_score - 5) * self.keyVar / 2)
        score = score + (tlinks_score - 5) * self.keyVar / 3
        score = score + ((title_score - 5) * self.keyVar)
        score = score + ((url_score - 5) * self.keyVar)
        score = score + anchorLinks - 5
        return int(score), report
