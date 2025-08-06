# livechat/forms.py
from django import forms
from .models import AvailabilitySlot, Appointment
from django.contrib.auth.models import User

class AvailabilitySlotForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = AvailabilitySlot
        fields = ['start_time', 'end_time']
        # counselor will be set in the view

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
        return cleaned_data

class AppointmentBookingForm(forms.Form):
    counselor = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), label="Choose Counselor") # Adjust queryset
    slot = forms.ModelChoiceField(queryset=AvailabilitySlot.objects.none(), label="Choose Slot")

    def __init__(self, *args, **kwargs):
        counselor_id = kwargs.pop('counselor_id', None)
        super().__init__(*args, **kwargs)
        if counselor_id:
            self.fields['slot'].queryset = AvailabilitySlot.objects.filter(
                counselor_id=counselor_id,
                is_booked=False
            ).order_by('start_time')
        else:
            # Initially show slots for all available counselors
            self.fields['slot'].queryset = AvailabilitySlot.objects.filter(
                is_booked=False
            ).order_by('counselor__username', 'start_time')