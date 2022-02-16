from django.db import models
from django import forms

# Create your models here.
class User(models.Model):
    ''' User info'''
    name = models.CharField(max_length=128,default='')
    key = models.CharField(max_length=32,default='S4od99')
    sid = models.CharField(max_length=64,unique=True)
    srlid = models.CharField(max_length=128,default='[0]')
    ft_quiz_answer = models.CharField(max_length=128,default='null')
    goal_quiz_answer = models.CharField(max_length=128,default='null')
    time_quiz_answer = models.CharField(max_length=128,default='null')
    help_quiz_answer = models.CharField(max_length=128,default='null')
    task_quiz_answer = models.CharField(max_length=128,default='null')
    environment_quiz_answer = models.CharField(max_length=128,default='null')
    evaluation_quiz_answer = models.CharField(max_length=128,default='null')


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
    plan = models.CharField(max_length=500)
    save_time = models.DateTimeField(auto_now=True)
    creat_time = models.DateTimeField(auto_now_add=True)
