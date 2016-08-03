import requests
import time
import iso8601
from django.http import Http404
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ExampleForm
from .models import AlgorithmVariable, Report, ReportURL
from .qscraper_utils import QscraperSEOQTool
from .majestic_utils import MajesticBackLinks
from .checker_utils import Checker_Utils
from .local_listing import LocalListing
from .mobilefriendlycheck import MobileFriendlyChecker
from .utils import get_expiration_and_creation_date,\
    get_built_with_information, get_total_time_and_ssl_certification
from .algorithm import Algorithm
from balystic.client import Client
from .email_report import send_simple_email


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
            'https://', '').replace('http://', '')
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
            'seoqtool:seoq_url_friendly_detail',
            slug=slug,
            netloc=netloc.replace('/', '--'))


class CreateVariableView(CreateView):

    model = AlgorithmVariable
    template_name = 'seoqtool/create_variable.html'
    fields = ['name', 'weight', 'active']

    def get_success_url(self):
        return reverse('seoqtool:variable_list')


class VariableListView(ListView):

    model = AlgorithmVariable
    template_name = 'seoqtool/variable_list.html'


class ReportView(View):

    template_name = 'seoqtool/report.html'

    def get(self, request, netloc):
        netloc = str(netloc)
        netloc = netloc.replace('--', '/')
        context = {'netloc': netloc}
        url = netloc.replace(
            'www.', '').replace(
            'https://', 'http://')
        if 'http://' not in url:
            url = 'http://' + url
        response = requests.get(url, verify=False)
        if response.status_code == 403:
            context['no_crawl_allowed'] = True
            return render(request, self.template_name, context)
        if response.status_code == 500:
            context['server_error'] = True
            return render(request, self.template_name, context)
        if response.status_code == 404:
            context['page_not_found'] = True
            return render(request, self.template_name, context)
        score = Algorithm().getSiteScore(netloc)
        context['score'] = score
        if request.user.is_authenticated():
            report = Report.objects.filter(
                netloc=netloc,
                user=request.user).latest('created')
            report.site_score = score
            report.save()
        else:
            report = Report.objects.filter(
                netloc=netloc).latest('created')
            report.site_score = score
            report.save()
        context['report'] = report
        return render(request, self.template_name, context)


class ArchiveReportView(View):
    template_name = 'seoqtool/score.html'
    client = Client()

    def get(self, request, netloc, year, month, day):
        netloc = str(netloc)
        netloc = netloc.replace('--', '/')
        context = {'netloc': netloc}
        url = netloc.replace(
            'www.', '').replace(
            'https://', 'http://')
        if 'http://' not in url:
            url = 'http://' + url
        try:
            report = Report.objects.filter(
                created__year=year,
                created__month=month,
                created__day=day,
                netloc=netloc).latest('created')
        except Report.DoesNotExist:
            raise Http404
        context['score'] = report.site_score
        context['keyword_score'] = report.keyword_score
        context['total_score'] = int(report.site_score +
                                     report.keyword_score)
        context['report'] = report
        error = 0
        improve = 0
        success = 0
        numeric_info = {
            'crawlability': {},
            'credibility': {},
            'conversation': {},
            'competition': {},
            'conversion': {},
            'content': {},
            'code': {},
        }
        for key, value in report.analysis.items():
            numeric_info[key]['total'] = len(value)
            local_error = 0
            local_success = 0
            local_improve = 0
            for inner_key, inner_value in value.items():
                if inner_value == 'error':
                    local_error += 1
                    error += 1
                elif inner_value == 'passed':
                    local_success += 1
                    success += 1
                elif inner_value == 'to improve':
                    local_improve += 1
                    improve += 1
            numeric_info[key]['errors'] = local_error
            numeric_info[key]['to_improve'] = local_improve
            numeric_info[key]['success'] = local_success
            numeric_info[key]['max'] = max(
                local_error, local_success, local_improve)
        context['numeric_info'] = numeric_info
        context['error'] = error
        context['passed'] = improve
        context['to_improve'] = success
        context['seo_professionals'] = self.client.get_users({'isPro':'1'})['users'][0:6]
        return render(request, self.template_name, context)

    def post(self, request, netloc, year, month, day):
        email = request.POST.get('email', None)
        if email is not None:
            send_simple_email(email, request.build_absolute_uri())
        return redirect(reverse(
            'seoqtool:archive_report',
            args=[netloc, year, month, day]))


class SEOQURLFriendlyDetail(View):
    """
    view to return the qscraper report
    from a friendly url, including
    the keywords and the url
    """
    template_name = 'seoqtool/report_example.html'

    def get(self, request, slug, netloc):
        keywords = str(slug.encode('utf-8')).replace('-', ' ')
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

        scraper = QscraperSEOQTool(
            netloc, keywordArray, 0, 1223, report=response.json())
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
        netloc = netloc.replace('--', '/')
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


class CreateReportURLView(LoginRequiredMixin, CreateView):
    template_name = 'seoqtool/create_urls.html'
    fields = ['frequency', 'url', 'keywords']
    model = ReportURL

    def get_context_data(self, *args, **kwargs):
        context = super(CreateReportURLView, self).get_context_data(
            *args, **kwargs)
        context['user_urls'] = self.request.user.reporturl_set.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.last_analyzed = timezone.now()
        return super(CreateReportURLView, self).form_valid(form)

    def get_success_url(self):
        success_url = reverse(
            'seoqtool:add_url')
        return success_url
