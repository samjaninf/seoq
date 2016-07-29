# 28 July 2016, Jessie Shen

from django.core.mail import send_mail
from django.http import HttpResponse


def sendSimpleEmail(emailto, reporturl, siteurl):
    subject = 'Your SEOQ Report is Ready!'
    message = 'Visit the link below to see your score report for your site ' + siteurl + '\n \n' + reporturl
    emailfrom = 'freddie@seoq.com'
    sendto = [emailto]
    send_mail(subject, message, emailfrom, sendto)
