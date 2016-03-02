from django.shortcuts import render
from django.http import HttpResponse
from .models import Learners
from .forms import *


def index(request):
    welcome_message = "Hello, visitor. You're at our Online Course System!"
    return HttpResponse(welcome_message)


def register_student(request):
    welcome_message = "You're Now at the student registration page."
    return HttpResponse(welcome_message)