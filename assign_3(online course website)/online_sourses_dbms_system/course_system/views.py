from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.template import Context

from .models import Learners
from .forms import LearnerForm


class LearnersRegistrationView(CreateView):
    form_class = LearnerForm
    model = Learners

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(Learners.objects.make_random_password())
        obj.save()

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'registration/verification.html',
            'subject_template_name': 'registration/verification_subject.txt',
            'request': self.request,
            # 'html_email_template_name': provide an HTML content template if you desire.
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        return redirect('accounts:register-done')


def index(request):
    welcome_message = "Hello, visitor. You're at our Online Course System!"
    return HttpResponse(welcome_message)


#def register_student(request):
