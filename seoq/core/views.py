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
        context = {'users': self.client.get_users(params={'isPro':'1'})}
        return render(request, self.template_name, context)
