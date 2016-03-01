from django.db import models
from django.core.validators import URLValidator #for dealing with urls

# Create your models here.
class learners(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    nick = models.CharField(max_length=12, unique=True)
    website = models.TextField(validators=[URLValidator()], null=True, blank=True)
    email = models.EmailField(max_length=69, unique=True, primary_key=True)
    #set password in views.py userform

class course(models.Model):
    coursename = models.CharField(max_length=42)
    courseID = models.AutoField(primary_key=True)
    about = models.CharField(max_length=999)
    provided_by_institute = models.CharField(max_length=99, default="freelance", blank=True)
    domain = models.CharField(max_length=33)



#class instructor(models.Model):
#    firstname = models.CharField(max_length=30)
#    lastname = models.CharField(max_length=30)