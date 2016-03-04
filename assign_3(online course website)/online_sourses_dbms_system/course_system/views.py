from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Learners
from .forms import *


def index(request):
    welcome_message = "Hello, visitor. You're at our Online Course System!"
    return HttpResponse(welcome_message)


def register_student(request):
    template = loader.get_template('course_system/index.html')
    #context = {
    #    'student_registration': student_registration,
    #}
    return HttpResponse(template.render(request))
