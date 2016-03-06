from django.conf.urls import url

from . import views

app_name = 'courseSystem'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register_student/$', views.register_student, name="register_student"),
    url(r'^register_teacher/$', views.register_teacher, name="register_teacher")
]
