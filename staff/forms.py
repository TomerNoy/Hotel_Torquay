from django import forms

from .models import *


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    # we're removing guest select for non staff members
    # added required get_form_kwargs to view
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        print(self.user.is_staff)

        if not self.user.is_staff:
            self.fields.pop("guest")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

        widgets = {
            'content': forms.Textarea()
        }
