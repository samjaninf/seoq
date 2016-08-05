from __future__ import absolute_import
import requests
from celery import shared_task
from .models import Report, ReportURL
from .algorithm import Algorithm
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone


@shared_task
def run_report(report_url):
    report_url = ReportURL.objects.get(pk=report_url)
    report = requests.post(
        settings.BASE_URL +
        reverse('api:start_report'), data={'url': report_url.url})
    if report.status_code != 200:
        error = report.json()['error']
        subject = "One of the websites for your periodic report failed!"
        message = "Your url " + report_url.url + 'returned a ' + str(error)
        message += ' status code. Please, check everything is all right'
        message += ' in your server'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [report_url.user],
            fail_silently=False,
        )
        return
    pk = report.json()['report']
    report = requests.post(
        settings.BASE_URL +
        reverse('api:site_score'), data={'pk': pk})
    redirect_url = report.json()['redirect_url']
    if report_url.keywords:
        requests.post(
            settings.BASE_URL +
            reverse('api:keyword_score'),
            data={'pk': pk, 'keywords': report_url.keywords})
    seoq_report_url = settings.BASE_URL + redirect_url
    subject = report_url.frequency + " report for " + report_url.url
    message = 'the ' + subject + ' has been created. to access it, please go '
    message += 'to ' + seoq_report_url
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [report_url.user],
        fail_silently=False,
    )


@shared_task
def run_all_reports():
    duration = {'daily': 1,
                'weekly': 7,
                'monthly': 30}
    now = timezone.now()
    report_urls = ReportURL.objects.all()
    for report in report_urls:
        time_delta = now - report.last_analyzed
        if time_delta.days >= duration[report.frequency]:
            run_report.delay(report.pk)
            report.last_analyzed = now
            report.save()
