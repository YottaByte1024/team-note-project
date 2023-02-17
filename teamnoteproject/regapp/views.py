from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegisterUserForm


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')
