import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from staff.filters import *
from staff.forms import *
from staff.models import *


def staff_home(request):
    bookings_count = len(Booking.objects.all())
    messages_count = len(Message.objects.all())
    reviews_count = len(Review.objects.all())

    context = {
        'bookings_count': bookings_count,
        'messages_count': messages_count,
        'reviews_count': reviews_count
    }
    return render(request, 'staff_home.html', context)


def list_bookings_view(request):
    f = BookingFilter(request.GET, queryset=Booking.objects.all())
    context = {'filter': f}
    return render(request, 'list_bookings.html', context)


def list_messages_view(request):
    msgs = Message.objects.all()
    context = {'msgs': msgs}
    return render(request, 'list_messages.html', context)


def list_reviews_view(request):
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'list_reviews.html', context)


def view_bookings_view(request, pk):
    booking = Booking.objects.get(pk=pk)
    context = {'booking': booking}
    return render(request, 'view_booking.html', context)


class MakeBookingsView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    template_name = 'make_booking.html'
    success_url = reverse_lazy('staff_home')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        check_in = self.object.check_in
        check_out = self.object.check_out

        room_id = self.object.room.id
        room_bookings = Booking.objects.filter(room_id=room_id)

        # check if room available:
        is_avail = True
        for booking in room_bookings:
            diff1 = (booking.check_in - check_out).days  # negative means check_out is after booking.check_in
            diff2 = (check_in - booking.check_out).days  # negative means check_in is before booking.check_out

            if diff1 < 0 and diff2 < 0:
                is_avail = False
        if is_avail:
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponse("ROOM UNAVAILABLE")


class DeleteBookingView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'delete_booking.html'
    success_url = reverse_lazy('bookings')


class DeleteMessageView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'delete_message.html'
    success_url = reverse_lazy('messages')


class EditBookingView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'edit_booking.html'
    success_url = reverse_lazy('bookings')


class MakeReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review_form.html'
    form_class = ReviewForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.guest = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'delete_review.html'
    success_url = reverse_lazy('reviews')


def previous_visits_view(request, username):
    visits = Booking.objects.filter(guest__user__username=username, check_in__lte=datetime.datetime.now())
    context = {'visits': visits, 'username': username}
    return render(request, 'previous_visits.html', context)
