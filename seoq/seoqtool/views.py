import requests
from django.conf import settings
from django.http import Http404
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AlgorithmVariable, ReportURL
from django.contrib.auth import get_user_model
from balystic.client import Client
from .email_report import send_simple_email

User = get_user_model()


class CreateVariableView(CreateView):

    model = AlgorithmVariable
    template_name = 'seoqtool/create_variable.html'
    fields = ['name', 'weight', 'active']

    def get_success_url(self):
        return reverse('seoqtool:variable_list')


class VariableListView(ListView):

    model = AlgorithmVariable
    template_name = 'seoqtool/variable_list.html'


class ArchiveReportView(View):
    template_name = 'seoqtool/score.html'
    client = Client()

    def get(self, request, netloc, year, month, day):
        netloc = str(netloc)
        report = requests.get(
            settings.QSCRAPER_URL + '/api/' +
            netloc + '/' + year + '/' + month + '/' +
            day + '/')
        if report.status_code == 404:
            raise Http404
        report = report.json()
        netloc = netloc.replace('--', '/')
        context = {
            'netloc': netloc}
        context['score'] = report['site_score']
        context['keyword_score'] = report['keyword_score']
        context['total_score'] = int(report['site_score'] +
                                     report['keyword_score'])
        if report['user']:
            report['user'] = User.objects.get(
                username=report['user'])
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
        for key, value in report['analysis'].items():
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
        context['passed'] = success
        context['to_improve'] = improve
        context['seo_professionals'] = self.client.get_users(
            {'isPro': '1', 'random': 'true'})['users'][0:6]
        return render(request, self.template_name, context)

    def post(self, request, netloc, year, month, day):
        put = request.POST.get('put', None)
        if put is not None:
            return self.put(request, netloc, year, month, day)
        email = request.POST.get('email', None)
        if email is not None:
            send_simple_email(email, request.build_absolute_uri())
            messages.success(
                request,
                'Your report was sent successfully to %s.' % email)
        return redirect(reverse(
            'seoqtool:archive_report',
            args=[netloc, year, month, day]))

    def put(self, request, netloc, year, month, day):
        if self.request.user.userplan.plan is None or\
           self.request.user.userplan.plan.default:
            messages.error(
                self.request, 'you need a plan to perform this action')
            return redirect(reverse('pricing'))
        netloc = str(netloc)
        requests.put(
            settings.QSCRAPER_URL + '/api/' +
            netloc + '/' + year + '/' + month + '/' +
            day + '/', data={'username': request.user.username})
        messages.success(request, 'You are sponsoring this report')
        return redirect(reverse(
            'seoqtool:archive_report',
            args=[netloc, year, month, day]))


class CreateReportURLView(LoginRequiredMixin, CreateView):
    template_name = 'seoqtool/create_urls.html'
    fields = ['frequency', 'url', 'keywords']
    model = ReportURL

    def get(self, *args, **kwargs):
        if self.request.user.userplan.plan is None or\
           self.request.user.userplan.plan.default:
            messages.error(
                self.request, 'you need a plan to perform this action')
            return redirect(reverse('pricing'))
        else:
            return super(CreateReportURLView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.user.userplan.plan is None or\
           self.request.user.userplan.plan.default:
            messages.error(
                self.request, 'you need a plan to perform this action')
            return redirect(reverse('pricing'))
        else:
            return super(CreateReportURLView, self).post(*args, **kwargs)

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
