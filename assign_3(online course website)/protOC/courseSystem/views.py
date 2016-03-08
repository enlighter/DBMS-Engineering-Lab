from django.shortcuts import render, redirect, render_to_response
from django.http import *
from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms

from .models import MyUser, Learners
from .admin import UserCreationForm, UserChangeForm
from .forms import LearnersProfileForm


def index(request):
    template = loader.get_template('courseSystem/index.html')
    return HttpResponse(template.render(request))

def reg_student(request):
    logout(request)

    registered = False

    if request.POST :
        email = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        nick = request.POST['nick']
        website = request.POST['website']
        password1 = request.POST['password']
        password2 = request.POST['repeat_password']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        else:
            password = password2

        user = MyUser(email=email, password=password, firstname=firstname, lastname=lastname,
                                         website=website)
        user.save()
        learner = Learners(user=user, nick=nick)
        learner.save()

        registered = True

    else:
        print("POST method of submitting form is required!")

    return render(request,
            'courseSystem/student_login.html',
            {'registered': registered})


def register_student(request):
    logout(request)

    registered = False

    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        learners_profile_form = LearnersProfileForm(data=request.POST)

        if user_form.is_valid() and learners_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = learners_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True

        else:
            print( user_form.errors, learners_profile_form.errors )

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserCreationForm()
        learners_profile_form = LearnersProfileForm()

        #user = authenticate(username=username, password=password)
        #if user is not None:
        #    if user.is_active:
        #        login(request, user)
        #        return HttpResponseRedirect('/main/')

    # Render the template depending on the context.
    return render(request,
            'courseSystem/student_login.html',
            {'user_form': user_form, 'profile_form': learners_profile_form, 'registered': registered})

def register_teacher(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
    return render_to_response('courseSystem/teacher_login.html', context_instance=RequestContext(request))
