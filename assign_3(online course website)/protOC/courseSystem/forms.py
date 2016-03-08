from django import forms

from .models import *
#from .admin import UserCreationForm, UserChangeForm

class LearnersProfileForm(forms.ModelForm):
    class Meta:
        model = Learners
        fields = ('user', 'nick')