import requests
import time
import iso8601
from django.shortcuts import render
from django.http import Http404
from django.views.generic import View
from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView, ListView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .forms import ExampleForm
from .models import AlgorithmVariable
from .utils import get_expiration_and_creation_date
from .utils import get_built_with_information
from .qscraper_utils import QscraperSEOQTool
from .majestic_utils import MajesticBackLinks
from .checker_utils import Checker_Utils
from .local_listing import LocalListing
from .mobilefriendlycheck import MobileFriendlyChecker
from .utils import get_expiration_and_creation_date,\
    get_built_with_information, get_total_time_and_ssl_certification
# Create your views here.


class BasicQscraperUseView(View):
    """
    Basic view that makes a basic request
    to the qscraper and renders a basic report
    with the data obtained.
    """
    template_name = 'seoqtool/report_example.html'
    formclass = ExampleForm

    def get(self, request):
        context = {'form': self.formclass(initial=request.GET)}
        url = request.GET.get('url', None)
        keywords = request.GET.get('keywords', None)
        depth = request.GET.get('depth', 0)
        if url is None or keywords is None:
            messages.error(
                request,
                'url and keywords required')
            return render(request, self.template_name, context)
        # gets each term, separated by comma, of the string
        keywords = [x.strip() for x in keywords.split(',') if x]
        keywords.sort()
        slug = ''
        slug = '-'.join(keywords)
        netloc = url.replace(
            'https://', '').replace('http://', '').replace('/', '')
        if not keywords:
            messages.error(
                request,
                'keywords required')
            return render(request, self.template_name, context)
        try:
            response = requests.post(
                settings.QSCRAPER_URL + '/api/seoq-tool/start-job/',
                json={'url': url,
                      'keywords': keywords,
                      'depth': depth})

        # if the external service is down, the site should stay up
        # and should provide feedback to the user about what
        # happened

        except requests.ConnectionError:
            messages.error(
                request,
                'the server is unavailable right now, please try again later.')
            return render(request, self.template_name, context)

        if response.status_code != 200:
            if response.status_code == 400:
                messages.error(
                    request,
                    response.json().get('error', 'unknown error'))
            else:
                messages.error(
                    request,
                    'An error has occurred, please try again later')
            return render(request, self.template_name, context)

        job_id = response.json()['job_id']
        non_stop = True

        # you need to keep verifying if the job has finish. Is better
        # to implement it using AJAX to avoid long waiting times from the
        # user. For this example, It will be done synchronously
        while non_stop:
            try:
                response = requests.get(
                    settings.QSCRAPER_URL +
                    '/api/status/' + job_id + '/')
                print response.json()['status'], job_id
                if response.status_code == 200 and\
                   response.json()['status'] == 'finished':
                    non_stop = False
            except requests.ConnectionError:
                messages.error(
                    request,
                    'the server is unavailable right now,' +
                    ' please try again later.')
                return render(request, self.template_name, context)
            # we want to avoid overcharging the qscraper server, so this
            # function guarantee that a request to the status page will
            # be done almost each 0.2 seconds
            # (you have to add it the time of execution of the rest
            # of the code inside the loop)
            time.sleep(0.2)
        try:
            response = requests.get(
                settings.QSCRAPER_URL +
                '/api/seoq/' + job_id + '/')
            context['report'] = response.json()
        except requests.ConnectionError:
            messages.error(
                request,
                'the server is unavailable right now,' +
                ' please try again later.')
            return render(request, self.template_name, context)
        # context['form'] = self.formclass(initial=request.GET)
        return redirect(
            'seoqtool:seoq_url_friendly_detail', slug=slug, netloc=netloc)


class CreateVariableView(CreateView):

    model = AlgorithmVariable
    template_name = 'seoqtool/create_variable.html'
    fields = ['name', 'weight', 'active']

    def get_success_url(self):
        return reverse('seoqtool:variable_list')


class VariableListView(ListView):

    model = AlgorithmVariable
    template_name = 'seoqtool/variable_list.html'


class SEOQURLFriendlyDetail(View):
    """
    view to return the qscraper report
    from a friendly url, including
    the keywords and the url
    """
    template_name = 'seoqtool/report_example.html'

    def get(self, request, slug, netloc):
        keywords = str(slug).replace('-', ' ')
        keywordArray = [x.strip() for x in keywords.split(' ') if x]
        netloc = str(netloc)
        context = {'keywords': keywords, 'netloc': netloc, 'slug': slug,
                   'keywordArray': keywordArray}
        date = request.GET.get('date', '')
        try:
            response = requests.get(
                settings.QSCRAPER_URL +
                '/api/seoq/' + slug +
                '/www/' + netloc + '/?date=' + date)

        # if the external service is down, the site should stay up
        # and should provide feedback to the user about what
        # happened

        except requests.ConnectionError:
            messages.error(
                request,
                'the server is unavailable right now, please try again later.')
            return render(request, self.template_name, context)

        if response.status_code != 200:
            if response.status_code == 404:
                raise Http404
            elif response.status_code == 400:
                messages.error(
                    request,
                    response.json().get('error', 'unknown error'))
            else:
                messages.error(
                    request,
                    'An error has occurred, please try again later')
                return render(request, self.template_name, context)

        scraper = QscraperSEOQTool(netloc, keywordArray, 0, 1223)
        majestic = MajesticBackLinks()
        checker = Checker_Utils()
        local = LocalListing()
        mobile = MobileFriendlyChecker()

        context['report'] = response.json()

        context['report']['recent_reports'] = sorted(set([
            iso8601.parse_date(report_date).date() for
            report_date in context['report']['recent_reports']]))

        context['report']['date'] = iso8601.parse_date(
            context['report']['date'])
        context['domain_dates'] = get_expiration_and_creation_date(netloc)
        context['ssl_certificate'] = get_total_time_and_ssl_certification(
            netloc).get('ssl_certificate', None)
        context['speed_info'] = get_total_time_and_ssl_certification(
            netloc).get('speed_info', {})
        context['cms_information'] = get_built_with_information(
            netloc).get('cms', [])
        # if already in format http://www.example.com
        if (netloc.find('www.') != -1) & (netloc.find('http://') != -1):
            netloc = netloc
        # if in format www.example.com
        elif (netloc.find('www.') != -1) & (netloc.find('http://') == -1):
            netloc = 'http://' + netloc
        # if in format example.com
        elif (netloc.find('www.') == -1) & (netloc.find('http://') == -1):
            netloc = 'http://www.' + netloc
        # if in format http://example.com
        elif (netloc.find('www.') == -1) & (netloc.find('http://') != -1):
            netloc = netloc.replace('http://', 'http://www.')
        response = requests.get(netloc)
        context['url'] = scraper.get_url(netloc)
        context['page_title'] = scraper.get_title()
        context['metadescription'] = scraper.get_meta_description()
        context['heading_score'] = scraper.calculate_headings()
        context['tlink_score'] = scraper.calc_tlinks()
        context['title_score'] = scraper.calculate_title()
        context['url_score'] = scraper.calculate_url()
        context['backlinks_domain'] = majestic.getNumBackLinksDomainName(
            netloc)
        context['baclinks_url'] = majestic.getNumBackLinksWebPageURL(netloc)
        context['govlinks_domain'] = majestic.getNumGovBackLinksDomainName(netloc)
        context['govlinks_url'] = majestic.getNumGovBackLinksWebPageURL(netloc)
        context['edulinks_domain'] = majestic.getNumEduBackLinksDomainName(netloc)
        context['edulinks_url'] = majestic.getNumEduBackLinksWebPageURL(netloc)
        context['robots'] = checker.checkRobots(netloc)
        context['local_listing'] = local.main(netloc)
        context['mobile'] = mobile.checkMobileFriendly(netloc)
        return render(request, self.template_name, context)
