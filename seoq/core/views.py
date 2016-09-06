import json
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.views.generic.base import RedirectView
from django.http import Http404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from balystic.client import Client
from seoq.users.models import User
from .forms import UserContactForm


class SEODirectoryUserList(View):
    """
    Displays a list of the users retrieved from 7dhub
    """
    template_name = 'pages/users_directory_page.html'
    client = Client()

    def get(self, request):
        alphabetical = request.GET.get('alphabetical', None)
        query_term = request.GET.get('q', None)
        if query_term is None:
            params = {'isPro': '1', 'alphabetical': '1'}
        else:
            params = {'isPro': '1', 'q': query_term}
        context = {
            'users': self.client.get_users(params=params),
            'query_term': query_term
        }
        context['most_view_users'] = Client().get_users(
            {'sort_type': 'view_count'})['users'][:3]
        context['most_recent_users'] = Client().get_users(
            {'sort_type': 'last_created'})['users'][:3]
        context['most_votes_answer_users'] = Client().get_users(
            {'sort_type': 'answer_vote_count'})['users'][:3]
        context['verified_users'] = Client().get_users(
            {'sort_type': 'verified'})['users'][:3]
        return render(request, self.template_name, context)


class PublicUserDetailView(View):
    template_name = 'users/public_user_detail.html'
    form_class = UserContactForm

    def get(self, request, username):
        user = Client().get_user_detail(username)
        data = user['user'].copy()
        if not isinstance(data['generics'], dict):
            data['generics'] = json.loads(data['generics'])
        data.pop('avatar')
        username = data.pop('username')
        if "error" in user:
            raise Http404
        try:
            data['generics']['view_count'] += 1
        except (KeyError, TypeError):
            data['generics']['view_count'] = 1
        data['generics'] = json.dumps(data['generics'])
        Client().update_user(user['user']['username'], data)
        try:
            user_local = User.objects.get(username=username)
        except User.DoesNotExist:
            user_local = User()
        return render(
            request,
            self.template_name,
            {'user': user, 'user_local': user_local, 'form': self.form_class})

    def post(self, request, username):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            location = request.POST.get('location')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            content = request.POST.get('content')
            template = 'users/contact_template.html'
            template = render_to_string(
                template,
                {'form_content': content,
                 'contact_name': first_name + ' ' + last_name,
                 'contact_email': email,
                 'location': location,
                 'phone': phone})
            send_mail(
                first_name + " wants to contact you!",
                None,
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data['email']],
                html_message=template,
                fail_silently=False)
            messages.success(request, 'Email sent to ' + username)

            return redirect(
                reverse('public_profile', kwargs={'username': username}))


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


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['qscraper_url'] = settings.QSCRAPER_URL
        return context
