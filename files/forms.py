from django import forms
from .models import TextFile, ExternalFile

class TextFileForm(forms.Form):
    Name = forms.CharField(max_length=100)
    Text = forms.CharField(widget=forms.Textarea)

class ExternalFileForm(forms.ModelForm):
    class Meta:
        model = ExternalFile
        fields = "__all__"
        widgets = {'FolderName':forms.HiddenInput(),
                    'Note':forms.Textarea()}

