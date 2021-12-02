from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import UserForm, MyAuthenticationForm


class MySignupView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'
    extra_context = {'item_type': 'User', 'form_type': 'Create'}

    def form_valid(self, form):
        self.object = form.save()
        user = authenticate(self.request, username=self.object.username, password=form.cleaned_data['password1'])
        if user:
            login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class DaLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = MyAuthenticationForm


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
