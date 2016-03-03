from django.conf.urls import url
from django.contrib.auth import views as View

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^register_student/$', views.LearnersRegistrationView.as_view(), name="register_student"),

    url(r'^register_student/done/$', View.password_reset_done, {
        'template_name': 'registration/initial_done.html',
    }, name='learner_register_done'),

    url(r'^register/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        View.password_reset_confirm, {
        'template_name': 'registration/initial_confirm.html',
        'post_reset_redirect': 'accounts:register-complete',
    }, name='register-confirm'),
    url(r'^register/complete/$', View.password_reset_complete, {
        'template_name': 'registration/initial_complete.html',
    }, name='register-complete'),
]