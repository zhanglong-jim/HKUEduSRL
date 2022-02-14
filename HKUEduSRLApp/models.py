from django.db import models
from django import forms

# Create your models here.
class User(models.Model):
    ''' User info'''
    name = models.CharField(max_length=128)
    uid = models.CharField(max_length=32,unique=True)
    sid = models.CharField(max_length=64,unique=True)
    srlid = models.CharField(max_length=128)
    ft_quiz_answer = models.CharField(max_length=128)
    goal_quiz_answer = models.CharField(max_length=128)
    time_quiz_answer = models.CharField(max_length=128)
    help_quiz_answer = models.CharField(max_length=128)
    task_quiz_answer = models.CharField(max_length=128)
    environment_quiz_answer = models.CharField(max_length=128)
    evaluation_quiz_answer = models.CharField(max_length=128)


    def __str__(self):
        return self.sid


class Saveoutput(models.Model):
    '''
    User Log data
    Just saved the output of sutdents
    Connect with User used sid
    Saved json of jsmind
    '''
    sid = models.CharField(max_length=64)
    srlid = models.CharField(max_length=64)
    output = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    save_time = models.DateTimeField(auto_now=True)
    creat_time = models.DateTimeField(auto_now_add=True)
