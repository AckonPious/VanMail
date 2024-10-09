from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from authentication.models import User
from mail.models import *

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'is_admin', 'is_registry', 'email', 'full_name', 'location','password1', 'password2']
        
        

class FinalSubmissionForm(ModelForm):
    class Meta:
        model = MailBox
        fields = ['assigned_to']
        
        


            
class MailReceiveForm(forms.Form):
    mails = forms.ModelMultipleChoiceField(
        queryset=Mail.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        mail_box = kwargs.pop('mail_box', None)
        super().__init__(*args, **kwargs)
        
        if mail_box:
            # Filter mails for the given mailbox
            self.fields['mails'].queryset = Mail.objects.filter(mail_box=mail_box)
            
            # Set checked by default for is_received mails
            self.initial['mails'] = [mail.id for mail in self.fields['mails'].queryset if mail.is_received]
