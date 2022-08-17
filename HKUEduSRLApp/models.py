from django.db import models
from django import forms
from pathlib import Path
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
    user_coursesid = models.CharField(max_length=500,default='[0]')
    user_style = models.CharField(max_length=128,default='block') #none屏蔽，block显示
    user_dashboard = models.CharField(max_length=128, default='block')  #none屏蔽，block显示
    user_L = models.CharField(max_length=128, default='en')  # en为英文默认，cn为简体中文

    def __str__(self):
        return self.sid

class Root_User(models.Model):
    ''' Root User info'''
    name = models.CharField(max_length=128,default='')
    password = models.CharField(max_length=32,default='laoqiu')

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

class courses(models.Model):
    coursesid = models.CharField(max_length=64)
    teacher = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    detail = models.CharField(max_length=1500)
    c_syllabus = models.CharField(max_length=1500,default='null')
    list = models.CharField(max_length=1500)
    tasknum = models.CharField(max_length=16)
    task_list = models.CharField(max_length=500)
    task_topic = models.CharField(max_length=500,default="{}")
    creat_time = models.DateTimeField(auto_now_add=True)

class pool(models.Model):
    poolid = models.CharField(max_length=64)
    video = models.CharField(max_length=64)
    source = models.CharField(max_length=64,default='0')
    Handouts = models.CharField(max_length=1500,default='null')
    context1 = models.CharField(max_length=500,default='null')
    context2 = models.CharField(max_length=500,default='null')
    context3 = models.CharField(max_length=500,default='null')
    creat_time = models.DateTimeField(auto_now_add=True)

class user_courses(models.Model):
    user_coursesid = models.CharField(max_length=64)
    coursesid = models.CharField(max_length=64)
    submit_data = models.CharField(max_length=1500,default='null')
    submit_url = models.CharField(max_length=256,default='null')
    answer1 = models.CharField(max_length=500, default='')
    answer2 = models.CharField(max_length=500, default='')
    answer3 = models.CharField(max_length=500, default='')
    f_poollist = models.CharField(max_length=128)
    r_poollist = models.CharField(max_length=128)
    # creat_time = models.DateTimeField(auto_now_add=True)

class Fujian(models.Model):
    name = models.CharField(max_length=32,verbose_name="附件名称")
    file = models.FileField(upload_to="upload/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name