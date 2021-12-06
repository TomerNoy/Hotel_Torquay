from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import ProfileForm
from staff.forms import BookingForm
from staff.models import *
from visitors.forms import MessageForm
from datetime import datetime, timedelta


# import pprint


class HomepageView(CreateView):
    model = Message
    template_name = 'homepage.html'
    form_class = MessageForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        # sorting room by avail date (up to a 30 days) to each room type and adding to context
        # context structure:
        # context = {
        #     'room_type': {
        #         'date': [room_list]
        #     },
        context = {}
        ctx = super(HomepageView, self).get_context_data(**kwargs)
        room_types = RoomType.objects.all()

        for room_type in room_types:
            context[room_type.name] = {}
            rooms_by_type = list(Room.objects.filter(room_type=room_type))
            print(rooms_by_type)
            available_rooms = []
            date_index = datetime.now().date()

            for i in range(30):
                for key, room in enumerate(rooms_by_type):
                    if not room.booking_set.all():
                        # if room doesn't have any booking at all to begin with, add it as avail
                        available_rooms.append(rooms_by_type.pop(key))
                    else:
                        is_booked = False
                        bookings = room.booking_set.all()
                        # check if already booked
                        for booking in bookings:
                            if booking.check_out >= date_index >= booking.check_in:
                                is_booked = True
                                break
                        if not is_booked:
                            available_rooms.append(rooms_by_type.pop(key))
                if available_rooms:
                    context[room_type.name][str(date_index)] = available_rooms
                # limit to 3 first avail dates
                if len(context[room_type.name].keys()) == 3:
                    break
                date_index += timedelta(days=1)
                available_rooms = []

        ctx['context'] = context
        # pprint.pprint(context)
        return ctx

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        if user:
            self.object.username = user.username
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UserBookingView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    template_name = 'usr_booking.html'
    success_url = reverse_lazy('usr_booking')
    login_url = 'login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

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
            if not self.request.user.is_staff:
                # print('--> not staff', self.request.user.profile.pk)
                self.object.guest = self.request.user.profile
                print(self.object)
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())  # todo fix err when not staff
        return HttpResponse("ROOM UNAVAILABLE")
