# from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.UserCreationView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls'))
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('profile', views.profile_view, name='profile'),
    # path('register_staff/', views.RegisterStaffView.as_view(), name='staff_register'),
]
