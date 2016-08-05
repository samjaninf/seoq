from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import RedirectView
from balystic.client import Client
from django.http import Http404
from django.core.urlresolvers import reverse
from django.conf import settings


class SEODirectoryUserList(View):
    """
    Displays a list of the users retrieved from 7dhub
    """
    template_name = 'pages/users_directory_page.html'
    client = Client()

    def get(self, request):
        query_term = request.GET.get('q', None)
        if query_term is None:
            params = {'isPro': '1'}
        else:
            params = {'isPro': '1', 'q': query_term}
        context = {
            'users': self.client.get_users(params=params),
            'query_term': query_term
        }
        return render(request, self.template_name, context)


class ArchivedBlogRedirectView(RedirectView):
    """
    Redirect Original blog entries patterns to the new one
    """
    client = Client()

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')

        blog_entry = self.client.get_blog_detail(slug)
        if 'blog' not in blog_entry:
            raise Http404

        return reverse(
            'balystic_blog_detail',
            kwargs={'slug': blog_entry['blog']['slug']})


class CompaniesRedirectView(RedirectView):
    """
    Temporary Redirect of SEO users profiles while profiles are moved
    """
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return settings.SEOQ_COMPANIES_URL + slug
