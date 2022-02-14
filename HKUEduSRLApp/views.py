import re

from django.http import HttpResponse

from . import models
# Create your views here.
from django.shortcuts import render,redirect
from django import forms
from django.db.models import Max
import datetime
import time

class UserForm(forms.Form):
    sid = forms.CharField(label="sid", max_length=64,widget=forms.TextInput(attrs={'placeholder': 'please input sid'}))
    username = forms.CharField(label="username", max_length=128,widget=forms.TextInput(attrs={'placeholder': 'please input name'}))
    uid = forms.CharField(label="uid", max_length=32,widget=forms.TextInput(attrs={'placeholder': 'please input uid'}))


def index(request):
    pass
    return render(request,'index.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect('/mysrl/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Please check first！"
        if login_form.is_valid():  # 确保用户名和密码都不为空
            sid = login_form.cleaned_data['sid']
            username = login_form.cleaned_data['username']
            uid = login_form.cleaned_data['uid']
            try:
                user = models.User.objects.get(sid=sid)
                if user.name == username:
                    if user.uid == uid:
                        request.session['is_login'] = True
                        request.session['user_sid'] = user.sid
                        request.session['user_name'] = user.name
                        request.session['user_uid'] = user.uid
                        if user.ft_quiz_answer=='':
                            return redirect('/ft/')
                        else :
                            return redirect('/mysrl/')
                    else:
                        message = "Wrong UID"
                else:
                    message = "Wrong name"
            except:
                message = "Unauthorized School ID No."
        return redirect("/ft/")
    login_form = UserForm()
    return render(request,'login.html',locals())
def ft(req):
    if not req.session.get('is_login', None):
        return redirect("/login/")
    sid = req.session.get('user_sid', None)
    user = models.User.objects.get(sid=sid)
    # print(user)
    print(req.GET.get('1'))
    if req.GET.get('1') is not None:
        if user.ft_quiz_answer == '':
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
def new(req):
    if not req.session.get('is_login', None):
        return redirect("/login/")
    sid = req.session.get('user_sid', None)
    print(sid)
    user = models.User.objects.get(sid=sid)
    user_srllist = user.srlid.replace('\'','')
    # print(user_srllist[-1])
    new = models.Saveoutput.objects.create()
    nuewsrlid= int(user_srllist[-1]) + 1
    new.srlid = nuewsrlid  # 新建srlid
    new.output = '{"meta":{"author":"ZhangLong","version":"0.2"},"format":"node_tree","data":{"id":"root","topic":"mysrl_name11","expanded":true}}'
    new.sid = sid
    new.name = req.session.get('user_name', None)
    new.save()
    user_srlidlistdata = '0'
    for i in range(nuewsrlid):
        user_srlidlistdata = user_srlidlistdata +',' + str(i+1)
    user.srlid = user_srlidlistdata
    # print(user.srlid)
    user.save()
    return redirect('/jsmind/'+'?id='+str(nuewsrlid))
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
    return render(request,'jsmind.html',locals())
def mysrl(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    sid = request.session.get('user_sid', None)
    # print(sid)
    user = models.User.objects.get(sid=sid)
    user_srllist = user.srlid.split(',')
    # print(user_srllist)
    datalist = []
    for i in user_srllist:
        if i == '0':
            continue
        else:
            info = models.Saveoutput.objects.filter(
                sid=sid, srlid= i
            ).last()
            temporary = {"srlid":info.srlid,"name": str(info.name),"creat_time":str(info.creat_time),"save_time":str(info.save_time)}
            datalist.append(temporary)
    # print(listjson)
    ans = user.ft_quiz_answer.replace('\'','')
    ans_r = ans.replace('[','')
    ans_r_p = ans_r.replace(']','')
    ans_l= ans_r_p.split(',')
    # print(ans_l)
    ans_show = []
    for i in ans_l:
        ans_show.append(int(i))
    # print(ans_show)
    Goal = int(sum(ans_show[0:5])/0.25)
    Evn = int(sum(ans_show[5:9])/0.20)
    Task = int(sum(ans_show[9:13])/0.20)
    Time = int(sum(ans_show[13:16])/0.15)
    Help = int(sum(ans_show[16:20])/0.20)
    Sel = int(sum(ans_show[20:24])/0.20)
    SRL_strategy = [Goal,Evn,Task,Time,Help,Sel]
    recomdation_s = min(SRL_strategy)
    recomdation_id= SRL_strategy.index(recomdation_s)
    if recomdation_id == 0:
        recomdation = 'Goal Setting'
        recomdation_url = '/Goal/'
    if recomdation_id == 1:
        recomdation = 'Enviroment Structuring'
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
        recomdation = 'Self-evalution'
        recomdation_url = '/Sel/'
    listjson = {"data": datalist,"SRL":SRL_strategy,'recomdation':recomdation,'recomdation_url':recomdation_url}
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