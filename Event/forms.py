
from .models import Event

from django.forms import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'
class EventForm(ModelForm):
    
    class Meta:
        model = Event
        fields = "__all__"

        widgets = {'description': Textarea(
            attrs={'cols': 10, 'rows': 10, 'class': 'form-control'}
        ), 'evt_date': DateInput(), 'title':TextInput(attrs={'class':'form-control'}), } 
        exclude=('state','nbr_paticipants','organisateur','participant',)

   