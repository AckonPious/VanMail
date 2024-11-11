from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User
from mail.models import *

 
class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'is_admin', 'is_registry', 'is_superadmin','email', 'full_name', 'location','password1', 'password2']
        
class MailBoxForm(forms.ModelForm):
    class Meta:
        model = MailBox
        fields = ['mail_id', 'handling_officer', 'to_location', 'remarks']
        
class MailsForm(forms.ModelForm):
    mail_description = forms.CharField(label='',
                   widget=forms.Textarea(attrs={'required':True}))
    class Meta:
        model = Mail
        fields = ['individual_mail_id', 'mail_description', 'priority_level', 'is_package', 'recalled']
              
class DriverForm(forms.ModelForm):
    class Meta:
        model = AssignedTo
        fields = ['name', 'phone_number']
        
        
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
        
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
            self.fields['mails'].queryset = Mail.objects.filter(mail_box=mail_box)
            self.initial['mails'] = [mail.id for mail in self.fields['mails'].queryset if mail.is_received]
