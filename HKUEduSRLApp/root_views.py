from django.http import HttpResponse, JsonResponse
from . import models
# Create your views here.
from django.shortcuts import render,redirect
from django import forms

class RootUserForm(forms.Form):
    rootname = forms.CharField(label="rootname", max_length=64,widget=forms.TextInput(attrs={'placeholder': 'Root Name'}))
    password = forms.CharField(label="password", max_length=32,widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


def root_login(request):
    if request.method == "POST":
        root_login_form = RootUserForm(request.POST)
        message = "Please check first！"
        if root_login_form.is_valid():  # 确保用户名和密码都不为空
            rootname = root_login_form.cleaned_data['rootname']
            password = root_login_form.cleaned_data['password']
            try:
                user = models.Root_User.objects.get(name=rootname)
                # if user.name == username:
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['rootname'] = rootname
                    request.session['stata'] = 'root'
                    return redirect("/management/")
                else:
                    message = "Wrong"
            except:
                message = "Login Failed"
    root_login_form = RootUserForm()
    return render(request,'root_login.html',locals())
def management(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.session.get('stata', None) != 'root':
        return redirect("/logout/")
    if request.method == 'POST':
        style = request.GET.get('style')
        if style =='pool':
            poolid = request.POST['poolid']
            video = request.POST['video']
            context1 = request.POST['context1']
            context2 = request.POST['context2']
            context3 = request.POST['context3']
            handouts = request.POST['handouts']
            try:
                pool = models.pool.objects.get(poolid= poolid)
            except:
                pool = models.pool.objects.create()
            pool.poolid = poolid
            pool.video=video
            pool.context1 = context1
            pool.context2 = context2
            pool.context3 = context3
            pool.handouts = handouts
            pool.save()
            print('Done:', poolid)
            message = 'pool saved, id is '+str(poolid)
            return render(request,'management.html',locals())
        elif style == 'course':
            courseid = request.POST['courseid']
            teacher = request.POST['teacher']
            name = request.POST['name']
            detail = request.POST['detail']
            tasknum = request.POST['tasknum']
            c_syllabus = request.POST['c_syllabus']
            list = request.POST['list']
            task_list = request.POST['task_list']
            task_topic = request.POST['task_topic']
            try:
                course = models.courses.objects.get(coursesid= courseid)
            except:
                course = models.courses.objects.create()
            course.coursesid = courseid
            course.teacher = teacher
            course.name = name
            course.detail = detail
            course.tasknum = tasknum
            course.c_syllabus = c_syllabus
            course.list = list
            course.task_list = task_list
            course.task_topic = task_topic
            course.save()
            print('Done:', courseid)
            message = 'course saved, id is '+ str(courseid)
            return render(request,'management.html',locals())
        else:
            message = 'error'
            return render(request,'management.html',locals())

    return render(request, 'management.html', locals())