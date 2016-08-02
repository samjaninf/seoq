import requests
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seoq.seoqtool.algorithm import Algorithm
from seoq.seoqtool.models import Report
# Create your views here.


class SiteFormView(APIView):
    """
    View that creates the report and returns its pk
    """

    def post(self, request):
        url = request.POST.get('url', None)
        response = requests.get(url, verify=False)
        if response.status_code == 403:
            return Response(
                {'error': response.status_code},
                status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == 500:
            return Response(
                {'error': response.status_code},
                status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == 404:
            return Response(
                {'error': response.status_code},
                status=status.HTTP_400_BAD_REQUEST)
        if url is None:
            return Response(
                {'error': 'url required'},
                status=status.HTTP_400_BAD_REQUEST)
        netloc = url.replace(
            'https://', '').replace('http://', '')
        if request.user.is_authenticated():
            report = Report.objects.create(netloc=netloc, user=request.user)
        else:
            report = Report.objects.create(netloc=netloc)
        return Response({'report': report.pk})


class KeywordsScoreView(APIView):

    def post(self, request, format=None):
        pk = request.POST.get('pk', None)
        keywords = request.POST.get('keywords', None)
        if keywords is None:
            raise Http404
        report = get_object_or_404(Report, pk=pk)
        keyword_score = Algorithm().getKeywordScore(report.netloc, keywords)
        report.keyword_score = keyword_score
        report.save()
        return Response({'redirect_url': report.get_absolute_url()})


class SiteScoreView(APIView):

    def post(self, request, format=None):
        pk = request.POST.get('pk', None)
        report = get_object_or_404(Report, pk=pk)
        score = Algorithm().getSiteScore(report.netloc)
        report.site_score = score
        report.save()
        return Response({'redirect_url': report.get_absolute_url()})
