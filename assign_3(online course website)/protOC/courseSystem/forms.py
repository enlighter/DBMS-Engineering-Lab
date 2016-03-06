from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import *

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        password = forms.CharField(widget=forms.PasswordInput)
        model = MyUser
        fields = UserCreationForm.Meta.fields + ('__all__',)
        widgets = {
            'password': forms.PasswordInput(),
        }


#    def save(self, commit=True):
#        user = super(MyUserCreationForm, self).save(commit=False)
#        user.email = self.cleaned_data["email"]
#        if commit:
#            user.save()
#        return user
