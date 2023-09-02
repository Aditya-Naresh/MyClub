from django import forms
from django.forms import ModelForm
from . models import Venue,Event


# Create a Venue Form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ("name","address","zip_code","phone","website","email_address")

        labels = {
            "name": "Enter Venue name",
            "address": "Enter Venu Address",
            "zip_code":"ZIP Code",
            "phone" : "Phone",
            "website" : "Link to the Website",
            "email_address" :"Email Address"
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'website':forms.TextInput(attrs={'class':'form-control'}),
            'email_address':forms.EmailInput(attrs={'class':'form-control'}),

        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'description','attendees')

        labels = {
            "Name": "Enter Event Name",
            "event_date": "YYYY-MM-DD",
            "venue":"Venue",
            "manager" : "Maanager",
            "description" : "Description",
            "attendees" :"Attendees"
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control','placeholder' : 'Event date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder' : 'Venue'}),
            'manager':forms.Select(attrs={'class':'form-select','placeholder' : 'Manager'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder' : 'Description'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-select','placeholder' : 'Attendees'}),

        }
