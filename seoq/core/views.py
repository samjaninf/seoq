from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import LoginForm


class LoginView(View):
    """
    View that handles the authentication form.
    """
    template_name = 'account/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect(settings.LOGIN_REDIRECT_URL)
                    else:
                        form.add_error(None, 'Account is not active')
            else:
                form.add_error(None, 'Not able to authenticate with the given credentials')
        return render(request, self.template_name, {'form': form})
