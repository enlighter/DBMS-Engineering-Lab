from django.db import models
from django.core.validators import URLValidator #for dealing with urls


# Create your models here.
class Learners(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    nick = models.CharField(max_length=12, unique=True)
    website = models.TextField(validators=[URLValidator()], null=True, blank=True)
    email = models.EmailField(max_length=69, unique=True, primary_key=True)
    #set password in views.py userform


class Course(models.Model):
    course_name = models.CharField(max_length=42)
    courseID = models.AutoField(primary_key=True)
    about = models.CharField(max_length=999)
    provided_by_institute = models.CharField(max_length=99, default="freelance", blank=True)
    domain = models.CharField(max_length=33)


class Instructor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=60, unique=True)
    website = models.TextField(validators=[URLValidator()], null=True, blank=True)
    instructorID = models.AutoField(primary_key=True)


class CourseContent(models.Model):
    courseID = models.ForeignKey(course, on_delete=models.CASCADE)
    partID = models.AutoField(primary_key=True)
    content_location = models.TextField(validators=[URLValidator()])
    content_name = models.CharField(max_length=30)
    content_type = models.CharField(max_length=18)
    has_evaluation = models.BooleanField()


class Performance(models.Model):
    score = models.TextField(max_length=10)
    partID = models.ForeignKey(course_content, on_delete=models.CASCADE)