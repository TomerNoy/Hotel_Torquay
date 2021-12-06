from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('usr_booking/<int:pk>/', views.UserBookingView.as_view(), name='usr_booking'),
]
