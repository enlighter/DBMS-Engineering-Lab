from django import forms
from .models import Learners


class LearnerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Learners
        fields = '__all__'