from __future__ import absolute_import
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
    report = Report.objects.create(
        site_score=Algorithm().getSiteScore(report_url.url),
        netloc=report_url.url.replace('http://', '').replace(
            'https://', '').replace('www.', ''),
        keyword_score=Algorithm().getKeywordScore(
            report_url.url, report_url.keywords),
        user=report_url.user)
    seoq_report_url = settings.BASE_URL + reverse(
        'seoqtool:archive_report',
        args=[report.netloc,
              report.created.strftime("%Y"),
              report.created.strftime("%m"),
              report.created.strftime("%d")])
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
