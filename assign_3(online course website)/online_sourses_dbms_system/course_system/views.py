from django.shortcuts import render, redirect, render_to_response
from django.http import *
from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Learners
from .forms import *


def index(request):
    template = loader.get_template('course_system/index.html')
    return HttpResponse(template.render(request))


def register_student(request):
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
    return render_to_response('course_system/student_login.html', context_instance=RequestContext(request))
    #context = {
    #    'student_registration': student_registration,
    #}
