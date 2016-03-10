import traceback
import logging
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect, render_to_response
from django.http import *
from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms

from .models import MyUser, Learners, Instructor
from .admin import UserCreationForm, UserChangeForm
from .forms import LearnersProfileForm

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('site.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def get_learner(user_object):
    if user_object is not None:
        try:
            return user_object.learners
        except:
            return None
    else:
        raise forms.ValidationError("Can't process an empty user object")

def get_instructor(user_object):
    if user_object is not None:
        try:
            return user_object.instructor
        except:
            return None
    else:
        raise forms.ValidationError("Can't process an empty user object")

def index(request):
    template = loader.get_template('courseSystem/index.html')
    return HttpResponse(template.render(request))

def register_student(request):
    logout(request)
    error = False
    error_msg = ''
    try:

        registered = False

        if request.POST :
            #debug log
            logger.info("Learner's login page")
            logger.info(str(request.POST))
            logger.info(str(request.POST['form_type']))

            if request.POST['form_type'] == 'register':
                #Process registration
                logger.info("Registration form used")
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

            elif request.POST['form_type'] == 'login':
                #Process login
                logger.info("Login form used")
                username = request.POST['username']
                password = request.POST['password']

                user = authenticate(username=username, password=password)
                logger.info("got " + str(user))

                if get_learner(user) is not None:
                    learner = user.learners
                    logger.info("Found an instructor instance for this user with nick : {0}".
                                format(learner.nick))
                    if learner is not None:
                        login(request, user=user)
                else:
                    raise forms.ValidationError("No learner account found for these login details!")


            else:
                logger.debug("invalid form type")
                raise forms.ValidationError("Invalid form type")

        else:
            print("POST method of submitting form is required!")

    except IntegrityError as e:
        error = True
        errno, strerror = e.args
        error_msg = "Encountered error: \nIntegrity error({0}): {1}".format(errno, strerror)

    except forms.ValidationError as e:
        error = True
        strerror = e.args
        error_msg = "Encountered error: \nValidation error: {0}".format(strerror)

    except:
        error = True
        error_msg = "Encountered error:" + traceback.format_exc(limit=1)

    return render(request,
            'courseSystem/student_login.html',
            {'registered': registered, 'error': error, 'error_msg': error_msg})


def register_teacher(request):
    logout(request)
    error = False
    error_msg = ''
    try:
        registered = False

        if request.POST :
            #debug log
            logger.info("Instructor's login page")
            logger.info(str(request.POST))
            logger.info(str(request.POST['form_type']))

            if request.POST['form_type'] == 'register':
                #Process registration
                logger.info("Registration form used")
                email = request.POST['username']
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
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
                teacher = Instructor(user=user)
                teacher.save()

                registered = True

            elif request.POST['form_type'] == 'login':
                #Process login
                logger.info("Login form used")
                username = request.POST['username']
                password = request.POST['password']

                user = authenticate(username=username, password=password)
                logger.info("got " + str(user))

                if get_instructor(user) is not None:
                    instructor = user.instructor
                    logger.info("Found an instructor instance for this user with id : {0}".
                                format(instructor.instructorID))
                    if instructor is not None:
                        login(request, user=user)
                else:
                    raise forms.ValidationError("No instructor account found for these login details!")

            else:
                logger.debug("invalid form type")
                raise forms.ValidationError("Invalid form type")

        else:
            print("POST method of submitting form is required!")

    except IntegrityError as e:
        error = True
        errno, strerror = e.args
        error_msg = "Encountered error: \nIntegrity error({0}): {1}".format(errno, strerror)
        logger.error(error_msg)

    except forms.ValidationError as e:
        error = True
        strerror = e.args
        error_msg = "Encountered error: \nValidation error: {0}".format(strerror)
        logger.error(error_msg)

    except:
        error = True
        error_msg = "Encountered error:" + traceback.format_exc(limit=1)
        logger.error(traceback.format_exc())

    return render(request,
            'courseSystem/teacher_login.html',
            {'registered': registered, 'error': error, 'error_msg': error_msg})
