from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import *


class UserCreationView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm()
        return context

    def form_valid(self, form):
        profile_form = ProfileForm(self.request.POST)
        if profile_form.is_valid():
            new_user = form.save()
            print(form.cleaned_data)
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            print(user)
            if user:
                login(self.request, user)
                print('logged in')
            return redirect('home')
        else:
            return self.form_invalid(form)


class MyLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        if self.request.user.is_staff:
            # return redirect('staff_home')
            return url or resolve_url('staff_home')

        return url or resolve_url(settings.LOGIN_REDIRECT_URL)
