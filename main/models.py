from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.


class Dreamreal(models.Model):
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    pid = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    passwd = models.CharField(max_length=50)

    class Meta:
        db_table = 'dreamreal'
        
class user_resume(models.Model):
    pid = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    user_resumestyle = models.CharField(max_length=50)
    user_skill = models.CharField(max_length=200)
    user_selfintroduction = models.CharField(max_length=2000)
    user_education = models.CharField(max_length=200)
    user_experience = models.CharField(max_length=2000)

    class Meta:
        db_table = 'user_resume'

