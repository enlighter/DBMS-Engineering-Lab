from django.db import models
from django.core.validators import URLValidator #for dealing with urls
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_marks(value):
    if (value < 0) or (value > 100) :
        raise ValidationError(
            _('%(value) is not a valid mark'),
            params={'value': value},
        )


def validate_status(value):
    if value not in ('audit','attempted','completed'):
        raise ValidationError(
            _('%(value) is not a valid status'),
            params={'value': value},
        )


# Create your models here.
class Learners(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    nick = models.CharField(max_length=12, unique=True)
    website = models.TextField(validators=[URLValidator()], null=True, blank=True)
    email = models.EmailField(max_length=69, unique=True, primary_key=True)
    #Many to Many relationship with course
    courses = models.ManyToManyField(Course)
    #set password in views.py userform


class Accomplishment(models.Model):
    status = models.CharField(max_length=9, default='audit', validators=[validate_status()], blank=True)
    performance = models.FloatField(null=True, blank=True)
    #Many to one relationship with course content
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #one to one relationship wwith a learner
    student = models.OneToOneField(Learners, on_delete=models.CASCADE, primary_key=True)


class Course(models.Model):
    course_name = models.CharField(max_length=42)
    courseID = models.AutoField(unique=True, primary_key=True)
    about = models.CharField(max_length=999)
    provided_by_institute = models.CharField(max_length=99, default="freelance", blank=True)
    domain = models.CharField(max_length=33)
    start_date = models.DateField()
    end_date = models.DateField()


class Instructor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=60, unique=True)
    website = models.TextField(validators=[URLValidator()], null=True, blank=True)
    instructorID = models.AutoField(unique=True, primary_key=True)
    #Many to many relationship with course
    courses = models.ManyToManyField(Course)


class CourseContent(models.Model):
    #Many to one relationship with course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    partID = models.AutoField(unique=True, primary_key=True)
    content_location = models.TextField(validators=[URLValidator()])
    content_name = models.CharField(max_length=30)
    content_type = models.CharField(max_length=18)
    has_evaluation = models.BooleanField()


class Performance(models.Model):
    score = models.IntegerField(validators=[validate_marks()])
    #Many to one relationship with course content
    course_content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    #one to one relationship wwith a learner
    student = models.OneToOneField(Learners, on_delete=models.CASCADE, primary_key=True)