from django import forms
from django.forms.widgets import DateInput

class EditForm(forms.Form):
    Title = forms.CharField(max_length = 200)
    Notes = forms.CharField(widget=forms.Textarea)
    Date = forms.DateField(widget = DateInput({'type':'date'}))
