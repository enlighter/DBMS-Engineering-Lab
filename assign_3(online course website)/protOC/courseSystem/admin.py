from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Learners)
admin.site.register(Instructor)
admin.site.register(Accomplishment)
admin.site.register(CourseContent)
admin.site.register(Performance)