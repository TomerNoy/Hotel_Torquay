from django import forms
from staff.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['username']

        widgets = {
            'message': forms.Textarea()
        }
