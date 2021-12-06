from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_home, name='staff_home'),
    # bookings
    path('list_bookings/', views.list_bookings_view, name='bookings'),
    path('view_booking/<int:pk>/', views.view_bookings_view, name='booking'),
    path('make_booking/', views.MakeBookingsView.as_view(), name='booking_form'),
    path('delete_booking/<int:pk>/', views.DeleteBookingView.as_view(), name='delete_booking'),
    path('edit_booking/<int:pk>/', views.EditBookingView.as_view(), name='edit_booking'),
    # messages
    path('list_messages/', views.list_messages_view, name='messages'),
    path('delete_message/<pk>/', views.DeleteMessageView.as_view(), name='delete_message'),
    path('previous_visits/<str:username>/', views.previous_visits_view, name='previous_visits'),
    # reviews
    path('make_review/', views.MakeReviewView.as_view(), name='review_form'),
    path('list_reviews/', views.list_reviews_view, name='reviews'),
    path('delete_review/<int:pk>/', views.DeleteReviewView.as_view(), name='delete_review'),
]
