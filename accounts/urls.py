from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.MySignupView.as_view(), name='signup'),
    path('login/', views.DaLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile', views.profile_view, name='profile'),
]
