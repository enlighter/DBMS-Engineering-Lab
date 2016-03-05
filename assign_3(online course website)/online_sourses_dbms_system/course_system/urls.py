from django.conf.urls import url

from . import views

app_name = 'course_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register_student/$', views.register_student, name="register_student")
]