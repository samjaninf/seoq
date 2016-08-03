from django.shortcuts import render
from django.views.generic import View
from balystic.client import Client


class SEODirectoryUserList(View):
    """
    Displays a list of the users retrieved from 7dhub
    """
    template_name = 'pages/users_directory_page.html'
    client = Client()

    def get(self, request):
        query_term = request.GET.get('q', None)
        if query_term is None:
            params={'isPro':'1'}
        else:
            params={'isPro':'1','q':query_term}
        context = {'users': self.client.get_users(params=params),'query_term': query_term}
        return render(request, self.template_name, context)
