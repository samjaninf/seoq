from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from seoq.seoqtool.algorithm import Algorithm
# Create your views here.


class KeywordsScoreView(APIView):

    def get(self, request, format=None):
        netloc = request.GET.get('url', None)
        keywords = request.GET.get('keywords', None)
        if netloc is None or keywords is None:
            raise Http404
        keyword_score = Algorithm().getKeywordScore(netloc, keywords)
        return Response({'keyword_score': keyword_score})
