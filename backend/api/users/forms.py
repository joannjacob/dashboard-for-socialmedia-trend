from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import UserProfile

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')

    class Meta:
        model = UserProfile
        fields = ('name', 'email',)