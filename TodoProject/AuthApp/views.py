from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView

from AuthApp.forms import CustomUserRegistrationForm, LoginForm
from AuthApp.models import CustomUser
from TaskApp.utils import TitleMixin


class RegistrationView(TitleMixin, CreateView):
    model = CustomUser
    template_name = 'register.html'
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form) -> HttpResponseRedirect:
        user = form.save(commit=False)
        user.save()

        login(self.request, user)

        messages.success(self.request, "Registration successful! Please log in!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "There were errors with registration")
        return super().form_invalid(form)

class CustomLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form) -> HttpResponseRedirect:
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        try:
            user = CustomUser.objects.get(username=username)

            if user.check_password(password):
                login(self.request, user)
                messages.success(self.request, "You have successfully logged in")
                return redirect(self.success_url)
            else:
                return self.form_invalid(form)
        except CustomUser.DoesNotExist:
            return self.form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = 'home'
    def get(self, request, *args, **kwargs):
        return redirect(self.get_next_page())

class UserProfile(LoginRequiredMixin, TitleMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'
    title = 'Profile'
    login_url = '/login/'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs['id'])

