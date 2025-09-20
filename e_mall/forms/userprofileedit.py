from django import forms
from e_mall.models.userprofile import Profile

class ProfileForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'rows':5,'cols':20, 'style':'resize:none;'}))
    class Meta:
        model = Profile
        fields = ['about']