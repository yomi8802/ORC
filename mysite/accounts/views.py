from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from .forms import SignupForm, LoginForm

class MySignupView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = '/orc/post_list'

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result


class MyLoginView(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class MyLogoutView(LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/logout.html'

class MyUserView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context