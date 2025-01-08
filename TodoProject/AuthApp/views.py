from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from AuthApp.forms import CustomUserRegistrationForm
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

