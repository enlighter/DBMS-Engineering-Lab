from django.conf.urls import url

from . import views

app_name = 'courseSystem'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register_student/$', views.register_student, name="register_student"),
    url(r'^register_teacher/$', views.register_teacher, name="register_teacher"),
    url(r'^student_login/$', views.register_student, name="student_login"),
    url(r'^teacher_login/$', views.register_student, name="teacher_login"),
    url(r'^all_courses/', views.all_courses, name="all_courses")
]
