import ast
import re
import uuid

from django.http import HttpResponse, JsonResponse
from . import models
# Create your views here.
from django.shortcuts import render,redirect
from django import forms
from django.db.models import Max
import datetime
import time
import json
# 注意！！！sid 是邮箱，uid是Key Code，我懒得改了
from .models import Fujian


class FujianForm(forms.ModelForm):
    class Meta:
        model = Fujian
        fields = ('file',)

def fujian_add(request):
    if request.method == 'POST':
        form = FujianForm(request.POST, request.FILES)
        if form.is_valid():
            fujian = form.save()
            data = {'is_valid': True, 'name': fujian.file.name, 'url': fujian.file.url}
        else:
            data = {'is_valid': False}
        # print(data['url'])
        user_courseid = int(request.GET.get('user_courseid'))
        course_task = int(request.GET.get('course_task'))
        user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
        course_task_list = tolist(models.courses.objects.get(coursesid=user_course.coursesid).task_list)
        user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
        submit_urls = ast.literal_eval(user_course.submit_url)
        submit_urls[course_task_list[course_task]] = data['url']
        print(str(submit_urls))
        user_course.submit_url = json.dumps(submit_urls)
        user_course.save()
        print('Done:', user_courseid, course_task)
        return JsonResponse(data)

def text(request):
    if request.method == 'POST':
        text = request.POST['data']
        user_courseid = int(request.GET.get('user_courseid'))
        course_task = int(request.GET.get('course_task'))
        user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
        course_task_list = tolist(models.courses.objects.get(coursesid=user_course.coursesid).task_list)
        user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
        submit_data = ast.literal_eval(user_course.submit_data)
        submit_data[course_task_list[course_task]] = text
        print(str(submit_data))
        user_course.submit_data = json.dumps(submit_data)
        user_course.save()
        print('Done:', user_courseid, course_task)
        return redirect("/homework/?user_courseid="+str(user_courseid)+"&course_task="+str(course_task))

def ans_submit(request):
    if request.method == 'POST':
        text = request.POST['data']
        user_courseid = int(request.GET.get('user_courseid'))
        taskid = int(request.GET.get('taskid'))
        poolid = int(request.GET.get('poolid'))
        qs = request.GET.get('qs')
        user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
        course_task_list = tolist(models.courses.objects.get(coursesid=user_course.coursesid).task_list)
        user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
        if qs =='question1':
            user_course.answer1 =text
        elif qs =='question2':
            user_course.answer2 =text
        elif qs =='question3':
            user_course.answer3 =text
        user_course.save()
        print('Done:', user_courseid, qs)
        if user_course.answer1 != '' and user_course.answer2 != '' and user_course.answer3 != '':
            finishtask(taskid,user_courseid,poolid)
            print('finish',user_courseid,taskid)
            return redirect("/index/")
        return redirect("/class/?taskid="+str(taskid)+"&poolid="+str(poolid)+"&user_courseid=%d"%user_courseid)

def finishtask(taskid,user_courseid,poolid):
    #完成task之后变更user_courseid中f_poollist、r_poollist
    user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
    f_poollist = tolist(user_course.f_poollist)
    r_poollist = tolist(user_course.r_poollist)
    f_poollist.append(str({taskid:poolid}).replace(' ',''))
    # print(str({taskid:poolid}))
    # print(r_poollist)
    # print(type(r_poollist[0]))
    r_poollist.remove(str({taskid:poolid}).replace(' ',''))
    # print(f_poollist)
    # print(r_poollist)
    user_course.f_poollist = str(f_poollist)
    user_course.r_poollist = str(r_poollist)
    user_course.save()

def classroom(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    # poolid =0
    taskid = request.GET.get('taskid')
    poolid = request.GET.get('poolid')
    user_courseid = request.GET.get('user_courseid')
    pool= models.pool.objects.get(poolid = poolid)
    user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
    courseid = user_course.coursesid
    course = models.courses.objects.get(coursesid=courseid)
    course_task_list = tolist(course.task_list)
    f_courseid = tolist(user_course.f_poollist)
    # print('f_courseid',f_courseid)
    f_course_list=[]
    f_poolid_list = []
    if f_courseid != ['']:
        for i in f_courseid:
            f_course_list.append(course_task_list[int(i.replace('{','').replace('}','').split(':')[0])])
            f_poolid_list.append(i.replace('{', '').replace('}', '').split(':')[1])
    r_courseid = tolist(user_course.r_poollist)
    # print('r_courseid', r_courseid)
    r_course_list = []
    r_poolid_list = []
    # print(r_courseid)
    if r_courseid != ['']:
        for i in r_courseid:
            r_course_list.append(course_task_list[int(i.replace('{','').replace('}','').split(':')[0])])
            r_poolid_list.append(i.replace('{', '').replace('}', '').split(':')[1])
    videosrc = pool.video
    context1 = pool.context1
    context2 = pool.context2
    context3 = pool.context3
    handouts = pool.Handouts
    print("handouts",handouts)
    answer1 = user_course.answer1
    answer2 = user_course.answer2
    answer3 = user_course.answer3
    listjson = {'videosrc':videosrc,'context1':context1,'context2':context2,'context3':context3,'handouts':handouts,
                'answer1':answer1,'answer2':answer2,'answer3':answer3,
                'f_course_list':f_course_list,'r_course_list':r_course_list,
                'f_poolid_list':f_poolid_list,'r_poolid_list':r_poolid_list,
                'user_courseid':user_courseid,'taskid':taskid,'poolid':poolid}
    return render(request,'videoclass.html',listjson)

def homework(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    user_courseid = int(request.GET.get('user_courseid'))
    course_task = int(request.GET.get('course_task'))
    user_course = models.user_courses.objects.get(user_coursesid=user_courseid)
    submit_data = ast.literal_eval(user_course.submit_data)
    submit_urls = ast.literal_eval(user_course.submit_url)
    course_task_list = tolist(models.courses.objects.get(coursesid=user_course.coursesid).task_list)
    task_topic_dist = ast.literal_eval(models.courses.objects.get(coursesid=user_course.coursesid).task_topic)
    task_topic = task_topic_dist[str(course_task)]
    last_url = submit_urls[course_task_list[course_task]]
    # print(course_task_list)
    for i in course_task_list:
        pass
    course_name = models.courses.objects.get(coursesid=user_course.coursesid).name
    listjson = {'user_courseid':user_courseid,'task_name':course_task_list[course_task],
                'course_task':course_task,
                'submit_data': submit_data[course_task_list[course_task]],
                'submit_urls': submit_urls[course_task_list[course_task]],
                'course_name': course_name,'last_url': last_url,
                'course_task_list':course_task_list,
                'task_topic':task_topic
                }
    return render(request, 'homework.html', listjson)
class UserForm(forms.Form):
    e_mail= forms.CharField(label="e_mail", max_length=64,widget=forms.TextInput(attrs={'placeholder': 'HKU Email'}))
    password = forms.CharField(label="password", max_length=32,widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Please check first！"
        if login_form.is_valid():  # 确保用户名和密码都不为空
            e_mail = login_form.cleaned_data['e_mail']
            # username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(sid=e_mail)
                print('e_mail:',e_mail)
                # if user.name == username:
                if user.key == password:
                    print('user:',user.sid,user.name,user.key,user.user_style)
                    request.session['is_login'] = True
                    request.session['user_sid'] = user.sid
                    request.session['user_name'] = user.name
                    request.session['user_style'] = user.user_style
                    request.session['user_dashboard'] = user.user_dashboard
                    request.session['user_language'] = user.user_L
                    if user.ft_quiz_answer == 'null':
                        return redirect("/ft/")
                    else:
                        return redirect("/index/")
                else:
                    message = "Wrong"
                # else:
                #     message = "Wrong name"
            except:
                message = "Login Failed"
    login_form = UserForm()
    return render(request,'login.html',locals())
class RegisterForm(forms.Form):
    e_mail= forms.CharField(label="e_mail", max_length=64,widget=forms.TextInput(attrs={'placeholder': 'HKU Email'}))
    password = forms.CharField(label="password", max_length=32,widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    re_password = forms.CharField(label="re_password", max_length=32,widget=forms.PasswordInput(attrs={'placeholder': 'Password again'}))
    name= forms.CharField(label="name", max_length=64,widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    language = forms.ChoiceField(choices=(("en","English"),("cn","简体中文")))
    key_code = forms.CharField(label="key_code", max_length=64,widget=forms.TextInput(attrs={'placeholder': 'Key Code'}))
def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Please check first！"
        if register_form.is_valid():  # 确保用户名和密码都不为空
            e_mail = register_form.cleaned_data['e_mail']
            password = register_form.cleaned_data['password']
            re_password = register_form.cleaned_data['re_password']
            name = register_form.cleaned_data['name']
            language = register_form.cleaned_data['language']
            key_code = register_form.cleaned_data['key_code']
            try:
                user = models.User.objects.get(sid=e_mail)
                message = "E_mail already existed"
                return render(request, 'register.html', locals())
            except:
                if password !=password:
                    message = "Password inconsistency"
                    return render(request, 'register.html', locals())
                else:
                    #处理keycode
                    if key_code=="S4od99":
                        coursesid=0#传入
                        r_poollist="['{0:'zl0'}', '{1:1}', '{2:2}','{3:3}']"
                    else:
                        message="Wrong key code. Please contact your teacher for it"
                        return render(request, 'register.html', locals())
                    #处理完毕
                    user=models.User.objects.create()
                    user.name=name
                    user.sid=e_mail
                    user.ft_quiz_answer = 'null'
                    user.environment_quiz_answer='null'
                    user.evaluation_quiz_answer='null'
                    user.goal_quiz_answer='null'
                    user.help_quiz_answer='null'
                    user.task_quiz_answer='null'
                    user.time_quiz_answer='null'
                    user.srlid="[0]"
                    user.key=password
                    user.user_L=language
                    user.user_dashboard="block"
                    user.user_style="block"
                    user_course=models.user_courses.objects.create()
                    user_coursesid=uuid.uuid4()
                    user_course.user_coursesid=user_coursesid
                    user.user_coursesid=[user_coursesid]
                    user.save()
                    user_course.coursesid=coursesid
                    user_course.f_poollist='[]'
                    user_course.r_poollist=r_poollist
                    course=models.courses.objects.get(coursesid=coursesid)
                    task_list=tolist(course.task_list)
                    submit_data={}
                    submit_url={}
                    for i in task_list:
                        submit_data[i]="null"
                        submit_url[i]="null"
                    user_course.submit_data=json.dumps(submit_data)
                    user_course.submit_url = json.dumps(submit_url)
                    user_course.answer1=''
                    user_course.answer2 = ''
                    user_course.answer3 = ''
                    user_course.save()
                if user.key == password:
                    print('user:',user.sid,user.name,user.key,user.user_style)
                    request.session['is_login'] = True
                    request.session['user_sid'] = user.sid
                    request.session['user_name'] = user.name
                    request.session['user_style'] = user.user_style
                    request.session['user_dashboard'] = user.user_dashboard
                    request.session['user_language'] = user.user_L
                    if user.ft_quiz_answer == 'null':
                        return redirect("/ft/")
                    else:
                        return redirect("/index/")
                else:
                    message = "Wrong"
    register_form = RegisterForm()
    return render(request,'register.html',locals())

def ft(req):
    if not req.session.get('is_login', None):
        return redirect("/login/")
    sid = req.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    print(sid)
    print(req.GET.get('1'))
    if req.GET.get('1') is not None:
        if user.ft_quiz_answer == 'null':
            ft_ans_list = []
            for i in range(24):
                ft_ans_list.append(req.GET.get(str(i + 1)))
            print(ft_ans_list)
            user.ft_quiz_answer = str(ft_ans_list)
            user.save()
            return redirect('/mysrl/')
        else:
            return redirect('/mysrl/')
    return render(req,'First time.html',locals())
# def new(req):
#     if not req.session.get('is_login', None):
#         return redirect("/login/")
#     sid = req.session.get('user_sid', None)
#     if req.method == 'POST':
#         user = models.User.objects.get(sid=sid)
#         user_srllist = user.srlid.replace('\'', '')
#         # print(user_srllist[-1])
#         new = models.Saveoutput.objects.create()
#         nuewsrlid = int(user_srllist[-1]) + 1
#         new.srlid = nuewsrlid  # 新建srlid
#         new.output = '{"meta":{"author":"ZhangLong","version":"0.2"},"format":"node_tree","data":{"id":"root","topic":"mysrl_name11","expanded":true}}'
#         new.sid = sid
#         new.name = req.session.get('user_name', None)
#         new.plan = '1:' + req.POST.get('1') + ',2:' + req.POST.get('2') + ',3:' + req.POST.get('3') + ',4:' + req.POST.get('4')
#         new.save()
#         user_srlidlistdata = '0'
#         for i in range(nuewsrlid):
#             user_srlidlistdata = user_srlidlistdata + ',' + str(i + 1)
#         user.srlid = user_srlidlistdata
#         # print(user.srlid)
#         user.save()
#         return HttpResponse({'success'})
#     else:
#         return HttpResponse('use POST request method please.')
def new(req):
    if not req.session.get('is_login', None):
        return redirect("/login/")
    sid = req.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    user_srllist = user.srlid.replace('\'', '').strip("[]").split(',')
    print(max(list(map(int, user_srllist))))
    new = models.Saveoutput.objects.create()
    nue_srlid = max(list(map(int, user_srllist))) + 1
    new_red = str(nue_srlid)
    user_srllist_update = str(list(range(nue_srlid +1)))
    new.srlid = new_red  # 新建srlid
    new.output = '{"meta":{"author":"ZhangLong","version":"0.2"},"format":"node_tree","data":{"id":"root","topic":"Enter topic","expanded":true,"children":[{"id":"f00efa19575318ce","topic":"Video activitiy","expanded":true,"direction":"right","children":[{"id":"f00f68eded68c10a","topic":"Plan1","expanded":true,"children":[{"id":"f00fab5818bbbc8e","topic":"How  much work","expanded":true},{"id":"f00fb079f2cdec3e","topic":"How much  time","expanded":true}]},{"id":"f00fa14f2a589c5d","topic":"Plan2","expanded":true,"children":[{"id":"f00fb642a735dc3a","topic":"How  much work","expanded":true},{"id":"f00fb9ea07d9a464","topic":"How much  time","expanded":true}]},{"id":"f00fa2d2da8e93d6","topic":"...","expanded":true}]},{"id":"f00f240b80ca3002","topic":"Reading activitiy","expanded":true,"direction":"right"},{"id":"f00f29db0bb4fe98","topic":"Discussion forum","expanded":true,"direction":"right"},{"id":"f00f2f4012e8ea93","topic":"Quiz","expanded":true,"direction":"right"},{"id":"f00f32fb3c026caa","topic":"Reflection paper","expanded":true,"direction":"right"},{"id":"f00f37e824233a95","topic":"Group project","expanded":true,"direction":"right"},{"id":"f00fa489154524ab","topic":"...","expanded":true,"direction":"right"}]}}'
    new.sid = sid
    new.name = req.session.get('user_name', None)
    new.save()
    # user_srlidlistdata = '0'
    # for i in range(nuewsrlid):
    #         user_srlidlistdata = user_srlidlistdata + ',' + str(i + 1)
    user.srlid = user_srllist_update
        # print(user.srlid)
    user.save()
    return redirect('/jsmind/'+'?id='+new_red)
def jsmind(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    # print(sid)
    #edit
    srlid = request.GET.get('id')
    # print(srlid)
    user = models.User.objects.get(sid=sid)
    user_srllist = user.srlid.split(',')

    info = models.Saveoutput.objects.filter(
        sid=sid, srlid=srlid
    ).last()
    # print(info.output)
    if request.session.get('user_language')=='cn':
        return render(request,'jsmind_cn.html',locals())
    return render(request,'jsmind.html',locals())
def todisk(a):
    tempdict = {}
    for i in a:
        tempdict[int(i.replace('{','').replace('}','').split(':')[0])]= int(i.replace('{','').replace('}','').split(':')[1])
    return tempdict
def tolist(a):
    a1=a.replace('\'','')
    a2=a1.replace('[','')
    a3=a2.replace(']','')
    # a4 = a3.replace(' ', '')
    # list = a4.split(',')
    list = a3.split(',')
    return list
def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    user_courseslist = tolist(user.user_coursesid)
    courseslist = []
    for i in user_courseslist:
        temp = models.user_courses.objects.get(user_coursesid = i).coursesid
        courseslist.append(temp)
    c_names =[]
    c_detail=[]
    c_syllabus =[]
    progress = []
    h_progress = []
    c_list = []
    r_next_poolid_list =[]
    r_next_taskid_list = []
    user_courses_list = []
    #[{'name',name}]
    for i in user_courseslist:
        print('i',i)
        user_courses = models.user_courses.objects.get(user_coursesid=i)
        course = models.courses.objects.get(coursesid=user_courses.coursesid)
        user_courses_list.append(user_courses.user_coursesid)
        print('name',course.name)
        c_names.append(course.name)
        c_detail.append(course.detail)
        c_syllabus.append(course.c_syllabus)
        tasknum =int(course.tasknum)
        f_poollist = tolist(user_courses.f_poollist)
        submit_data = ast.literal_eval(user_courses.submit_data)
        submit_urls = ast.literal_eval(user_courses.submit_url)
        r_next_poolid= tolist(user_courses.r_poollist)[0]
        r_next_poolid_value = r_next_poolid.replace('{','').replace('}','').split(':')
        # print('r_next_poolid_value',r_next_poolid_value)
        if r_next_poolid_value[-1] =='':
            r_next_poolid_list.append(f_poollist[-1].replace('{','').replace('}','').split(':')[-1])
            r_next_taskid_list.append(f_poollist[-1].replace('{', '').replace('}', '').split(':')[0])
        else:
            r_next_poolid_list.append(r_next_poolid_value[-1])
            r_next_taskid_list.append(r_next_poolid_value[0])
        f_poolnum = len(f_poollist)
        if f_poollist==['']:
            progress.append('0%')
        else:
            progress.append("%.2f%%" % (f_poolnum/tasknum * 100))
        submit_data_num = 0
        for i in range(tasknum):
            if list(submit_data.values())[i] != "null" and list(submit_urls.values())[i]:
                submit_data_num =submit_data_num +1
        if submit_data_num==0:
            h_progress.append('0%')
        else:
            h_progress.append("%.2f%%" % (submit_data_num/tasknum * 100))
        c_list.append(course.list)
        # print(h_progress)
    listjson = {"c_names": c_names,"c_detail": c_detail,"c_syllabus": c_syllabus,"progress": progress,"h_progress": h_progress,
                "c_list": c_list,'r_next_poolid_list':r_next_poolid_list,
                'user_courses_list':user_courses_list,'taskid':r_next_taskid_list}
    return render(request,'index.html',listjson)
def mysrl(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    # print(sid)
    user = models.User.objects.get(sid=sid)
    user_srllist = list(map(int,user.srlid.replace('\'', '').strip("[]").split(',')))
    # print(max(list(map(int, user_srllist))))
    datalist = []
    for i in user_srllist:
        if i == '0' or i ==0:
            continue
        else:
            info = models.Saveoutput.objects.filter(
                sid=sid, srlid= str(i)
            ).last()
            infofirst = models.Saveoutput.objects.filter(
                sid=sid, srlid=str(i)
            ).first()
            temporary = {"srlid":info.srlid,"name": str(info.name),"creat_time":str(infofirst.creat_time),"save_time":str(info.save_time)}
            datalist.append(temporary)
    # print(listjson)
    # print(user.ft_quiz_answer)
    if user.ft_quiz_answer == 'null':
        return redirect('/ft/')
    ans = user.ft_quiz_answer.replace('\'','')
    ans_r = ans.replace('[','')
    ans_r_p = ans_r.replace(']','')
    ans_l= ans_r_p.split(',')
    # print(ans_l)
    ans_show = []
    for i in ans_l:
        ans_show.append(int(i))
    # print(ans_show)
    if len(ans_show)>7:
        Goal = int(sum(ans_show[0:5]) / 0.25)
        # print(Goal)
        if user.goal_quiz_answer != 'null':
            anslist = tolist(user.goal_quiz_answer)
            if anslist[0]=='D':
                Goal = Goal +10
                # print(Goal)
            if anslist[1]=='B':
                Goal = Goal +10
                # print(Goal)
            if anslist[2]=='B':
                Goal = Goal +10
                # print(Goal)
            if Goal >100:
                Goal = 100
        # print(Goal)
        Evn = int(sum(ans_show[5:9])/0.20)
        if user.environment_quiz_answer != 'null':
            anslist = tolist(user.environment_quiz_answer)
            if anslist[0]=='D':
                Evn = Evn +6
            if anslist[1]=='B':
                Evn = Evn +6
            if anslist[2]=='True':
                Evn = Evn +6
            if anslist[3]=='False':
                Evn = Evn +6
            if anslist[4]=='D':
                Evn = Evn +6
            if Evn >100:
                Evn = 100
        Task = int(sum(ans_show[9:13])/0.20)
        if user.task_quiz_answer != 'null':
            anslist = tolist(user.task_quiz_answer)
            if anslist[0]=='C':
                Task = Task +3.5
            if anslist[1]=='D':
                Task = Task +3.5
            if anslist[2]=='B':
                Task = Task +3.5
            if anslist[3]=='True':
                Task = Task +3.5
            if anslist[4]=='B':
                Task = Task +3.5
            if anslist[5]=='D':
                Task = Task +3.5
            if anslist[6]=='D':
                Task = Task +3.5
            if anslist[7]=='C':
                Task = Task +3.5
            if anslist[8]=='D':
                Task = Task +3.5
            if Task >100:
                Task = 100
        Time = int(sum(ans_show[13:16])/0.15)
        if user.time_quiz_answer != 'null':
            anslist = tolist(user.time_quiz_answer)
            if anslist[0] == 'D':
                Time = Time + 10
            if anslist[1] == 'C':
                Time = Time + 10
            if anslist[2] == 'True':
                Time = Time + 10
            if Time > 100:
                Time = 100
        Help = int(sum(ans_show[16:20])/0.20)
        if user.help_quiz_answer != 'null':
            anslist = tolist(user.help_quiz_answer)
            if anslist[0]=='False':
                Help = Help +6
            if anslist[1]=='D':
                Help = Help +6
            if anslist[2]=='C':
                Help = Help +6
            if anslist[3]=='False':
                Help = Help +6
            if anslist[4]=='D':
                Help = Help +6
            if Help >100:
                Help = 100
        Sel = int(sum(ans_show[20:24])/0.20)
        if user.evaluation_quiz_answer != 'null':
            anslist = tolist(user.evaluation_quiz_answer)
            if anslist[0]=='False':
                Sel = Sel +10
            if anslist[1]=='True':
                Sel = Sel +10
            if anslist[2]=='C':
                Sel = Sel +10
            if Help >100:
                Sel = 100
        SRL_strategy = [Goal,Evn,Task,Time,Help,Sel]
    recomdation_s = min(SRL_strategy)
    recomdation_id= SRL_strategy.index(recomdation_s)
    if recomdation_id == 0:
        recomdation = 'Goal Setting'
        recomdation_url = '/Goal/'
    if recomdation_id == 1:
        recomdation = 'Environment Structuring'
        recomdation_url = '/Env/'
    if recomdation_id == 2:
        recomdation = 'Task Strategies'
        recomdation_url = '/Task/'
    if recomdation_id == 3:
        recomdation = 'Time Management'
        recomdation_url = '/Time/'
    if recomdation_id == 4:
        recomdation = 'Help Seeking'
        recomdation_url = '/Help/'
    if recomdation_id == 5:
        recomdation = 'Self-evaluation'
        recomdation_url = '/Sel/'
    listjson = {"data": datalist,"SRL":SRL_strategy,'recomdation':recomdation,'recomdation_url':recomdation_url}
    if request.session.get('user_language')=='cn':
        return render(request,'mysrl_cn.html',listjson)
    return render(request,'mysrl.html',listjson)
def record_add(req):
    """
    添加解析记录
    :param req:
    :return:
    """
    if not req.session.get('is_login', None):
        return redirect("/login/")
    print(req.session.get('user_sid', None));
    if req.method == 'POST':
        data = req.POST.get('data')
        sid = req.POST.get('sid')
        srlid = req.POST.get('srlid')
        # stime = req.POST.get('stime')
        # print(data,sid)
        new_save = models.Saveoutput.objects.create()
        new_save.sid = sid
        new_save.srlid = srlid
        new_save.output = data
        name = re.findall(r"{\"id\":\"root\",\"topic\":\"(.+?)\"",data)
        print(name)
        new_save.name = name[0]
        new_save.save()
        return HttpResponse('scuess')
    else:
        return HttpResponse('use POST request method please.')

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect('/login/')
def Goal(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    if request.method=='GET':
        ans1 = request.GET.get('When')
        ans2 = request.GET.get('measurable')
        ans3 = request.GET.get('course')
        ans = [ans1,ans2,ans3]
        user.goal_quiz_answer = ans
        user.save()
    return render(request,'Goal.html',locals())
def Env(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    if request.method=='GET':
        ans1 = request.GET.get('1')
        ans2 = request.GET.get('2')
        ans3 = request.GET.get('3')
        ans4 = request.GET.get('4')
        ans5 = request.GET.get('5')
        ans = [ans1,ans2,ans3,ans4,ans5]
        user.environment_quiz_answer = ans
        user.save()
    return render(request,'Env.html',locals())
def Task(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    if request.method=='GET':
        ans1 = request.GET.get('1')
        ans2 = request.GET.get('2')
        ans3 = request.GET.get('3')
        ans4 = request.GET.get('4')
        ans5 = request.GET.get('5')
        ans6 = request.GET.get('6')
        ans7 = request.GET.get('7')
        ans8 = request.GET.get('8')
        ans9 = request.GET.get('9')
        ans = [ans1,ans2,ans3,ans4,ans5,ans6,ans7,ans8,ans9]
        user.task_quiz_answer = ans
        user.save()
    return render(request,'Task.html',locals())
def Time(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    if request.method=='GET':
        ans1 = request.GET.get('1')
        ans2 = request.GET.get('2')
        ans3 = request.GET.get('3')
        ans = [ans1,ans2,ans3]
        user.time_quiz_answer = ans
        user.save()
    return render(request,'Time.html',locals())
def Help(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    if request.method=='GET':
        ans1 = request.GET.get('1')
        ans2 = request.GET.get('2')
        ans3 = request.GET.get('3')
        ans4 = request.GET.get('4')
        ans5 = request.GET.get('5')
        ans = [ans1,ans2,ans3,ans4,ans5]
        user.help_quiz_answer = ans
        user.save()
    return render(request,'Help.html',locals())
def Sel(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    if request.method=='GET':
        ans1 = request.GET.get('1')
        ans2 = request.GET.get('2')
        ans3 = request.GET.get('3')
        ans = [ans1,ans2,ans3]
        user.evaluation_quiz_answer = ans
        user.save()
    return render(request,'Sel.html',locals())