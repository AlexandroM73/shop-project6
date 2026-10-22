# mailing/forms.py
from django import forms
from .models import Mailing
from django.utils import timezone

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'recipients']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time < timezone.now():
                raise forms.ValidationError('Дата начала не может быть в прошлом.')
            if start_time >= end_time:
                raise forms.ValidationError('Дата начала должна быть строго раньше даты окончания.')

        return cleaned_data
