from django import forms
from users.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {'user_passwd': forms.PasswordInput()}    
        fields = ('user_email', 'user_passwd')