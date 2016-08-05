# 28 July 2016, Jessie Shen

from django.core.mail import send_mail
from django.conf import settings


def send_simple_email(emailto, reporturl):
    subject = 'Your SEOQ Report is Ready!'
    message = 'Visit the link below to see your score report for your site!' +\
        '\n \n' + reporturl
    emailfrom = settings.DEFAULT_FROM_EMAIL
    sendto = [emailto]
    send_mail(subject, message, emailfrom, sendto)
