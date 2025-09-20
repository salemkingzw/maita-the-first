from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from allauth.account.forms import SignupForm

unallowed_characters="""`~!@#$%^&*()+-={|[:;}"',./?<>]"""
unallowed_characters_2="""`~!#$%^&*()={|[:;}"',?<>]"""

def validate_username(item):
    if ' ' in item:
        raise ValidationError ("username cannot contain spaces")
    if item[-1:] in unallowed_characters:
        raise ValidationError("that character isnt allowed at the end of username")    
    for itemss in item:
        if itemss in unallowed_characters_2:
            raise ValidationError("you can't use that character in a username")
    
def validate_email(item):
    if User.objects.filter(email=item).exists():
        raise ValidationError("email already used")

class MyCustomSignupForm(SignupForm):
    username=forms.CharField(validators=[validate_username])
    email=forms.CharField(widget=forms.EmailInput, validators=[validate_email])
    password1=forms.CharField(max_length=128, widget=forms.PasswordInput,validators=[validate_password])
    password2=forms.CharField(max_length=128, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email','password']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords don't match")
        return password1


