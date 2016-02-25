from django.db import models

# Create your models here.
class learners(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    nick = models.CharField(max_length=12)

class instructor(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)