# from asyncio.windows_events import NULL
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from main.models import Dreamreal, companyacc, companyacc_jobs
from django.core.mail import send_mail
import re
import string
import random
import datetime
import time
# Create your views here.

complete = []
complete_key = ''.join(random.choice(string.ascii_letters + string.digits)
                       for _ in range(10))
complete_key2 = ''
reset_complete = []
reset_complete_key = ''.join(random.choice(string.ascii_letters + string.digits)
                             for _ in range(12))
reset_complete_key2 = ''

com_complete = []
com_complete_key = ''.join(random.choice(string.ascii_letters + string.digits)
                           for _ in range(10))
com_complete_key2 = ''


def confirm(request):
    global complete
    global complete_key2
    try:
        if request.GET.get('k') == complete_key2:
            dreamreal = Dreamreal(
                lastname=complete[0],
                firstname=complete[1],
                pid=complete[2],
                email=complete[3],
                passwd=complete[4]
            )

            dreamreal.save()
            messages.add_message(
                request, messages.INFO, '註冊成功')
            return redirect('login')
        else:
            messages.add_message(
                request, messages.INFO, '驗證錯誤，請重新註冊!')
            return redirect('signIn')
    except:
        messages.add_message(
            request, messages.INFO, '帳號已驗證過!')
        return redirect('signIn')


def resetconfirm(request):
    global reset_complete
    global reset_complete_key2
    try:
        if request.GET.get('k') == reset_complete_key2:
            try:
                user = Dreamreal.objects.get(email=reset_complete[0])
            except:
                user = companyacc.objects.get(email=reset_complete[0])
            user.passwd = reset_complete[1]
            user.save()
            messages.add_message(
                request, messages.INFO, '密碼修改成功!')
            return redirect('login')
        else:
            messages.add_message(
                request, messages.INFO, '驗證錯誤，請重新修改!')
            return render(request, 'reset.html')
    except:
        messages.add_message(
            request, messages.INFO, '非預期錯誤!')
        return render(request, 'reset.html')


def signIn(request):
    if request.method == 'POST':
        lastname = request.POST['last_name']
        firstname = request.POST['first_name']
        pid = request.POST['pid']
        email = request.POST['email']
        passwd = request.POST['passwd']
        try:
            try:
                Dreamreal.objects.get(pid=pid)
            except:
                Dreamreal.objects.get(email=email)
            account_exist = 0
        except:
            account_exist = 1

        if account_exist:
            if '' in [lastname, firstname, pid, email, passwd]:
                messages.add_message(
                    request, messages.INFO, '資料不完整請重新輸入!')
                return render(request, 'signIn.html')
            elif None == re.search(r'[A-Z]{1}\d{9}', str(pid)):
                messages.add_message(
                    request, messages.INFO, '身分格式錯誤請重新輸入!')
                return render(request, 'signIn.html')
            elif None == re.search(r"\w+@\w+\.\w+", str(email)):
                messages.add_message(
                    request, messages.INFO, '信箱格式錯誤請重新輸入!')
                return render(request, 'signIn.html')
            else:
                # sendSimpleEmail(request, email)
                global complete_key
                global complete_key2
                global complete
                complete_key2 = complete_key
                lastname = str(lastname)
                firstname = str(firstname)
                pid = str(pid)
                email = str(email)
                passwd = str(passwd)
                complete = [lastname, firstname, pid, email, passwd]
                # send_mail("confirm mail", "進入此連結驗證:http://127.0.0.1:8000/main/confirm?k=%s" % complete_key2,
                #           "kevinliang1018@gmail.com", [email])
                send_mail("confirm mail", "進入此連結驗證:https://findjob2022project.herokuapp.com/main/confirm?k=%s" % complete_key2,
                          "kevinliang1018@gmail.com", [email])
                time.sleep(3)

                return HttpResponse('請至信箱驗證')
        else:
            messages.add_message(
                request, messages.INFO, '身分證或email已註冊過!')
            return render(request, 'signIn.html')
    else:
        return render(request, 'signIn.html')


def login(request):
    try:
        if 'status' in request.session:
            status = request.session['status']
            return render(request, 'index.html', context={'status': status})
        if 'account' in request.session:
            account = request.session['account']
            passwd = request.session['passwd']
            try:
                try:
                    user = Dreamreal.objects.get(pid=account)
                except:
                    user = Dreamreal.objects.get(email=account)
            except:
                try:
                    user = companyacc.objects.get(pid=account)
                except:
                    user = companyacc.objects.get(email=account)
            if passwd == user.passwd:
                return redirect('index')
            else:
                del request.session['account']
                del request.session['passwd']
        else:
            pass
    except:
        pass
    if request.method == 'POST':
        account = request.POST['account']
        passwd = request.POST['passwd']

        try:
            try:
                try:
                    user = Dreamreal.objects.get(pid=account)
                except:
                    user = Dreamreal.objects.get(email=account)
            except:
                try:
                    user = companyacc.objects.get(pid=account)
                except:
                    user = companyacc.objects.get(email=account)

            if user.passwd == passwd:
                request.session['passwd'] = user.passwd
                try:
                    request.session['status'] = str(user.companyname)
                except:
                    request.session['status'] = str(
                        user.firstname)+str(user.lastname)
                return redirect('index')
            else:
                messages.add_message(
                    request, messages.INFO, '帳號或密碼錯誤!')
                del request.session['account']
                return render(request, 'login.html')
        except:
            messages.add_message(
                request, messages.INFO, '帳號不存在!')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    try:
        try:
            del request.session['account']
            del request.session['passwd']
            del request.session['status']
        except:
            try:
                del request.session['passwd']
                del request.session['status']
            except:
                del request.session['status']
    except:
        pass
    return redirect("index")


def reset(request):
    if request.method == 'POST':
        global reset_complete
        global reset_complete_key
        global reset_complete_key2
        reset_complete_key2 = reset_complete_key
        account = request.POST['account']
        re_pass = request.POST['repass']
        chech_pass = request.POST['checkpass']
        try:
            try:
                user = Dreamreal.objects.get(email=account)
            except:
                user = companyacc.objects.get(email=account)
        except:
            messages.add_message(
                request, messages.INFO, '查無此帳號!')
            return render(request, 'reset.html')

        try:
            if user.passwd == re_pass:
                messages.add_message(
                    request, messages.INFO, '不可與原密碼相同!')
                return render(request, 'reset.html')
            elif '' in [re_pass]:
                messages.add_message(
                    request, messages.INFO, '密碼不可空白!')
                return render(request, 'reset.html')
            elif re_pass != chech_pass:
                messages.add_message(
                    request, messages.INFO, '密碼確認錯誤，請重新確認!')
                return render(request, 'reset.html')
            else:
                reset_complete = [user.email, re_pass]
                # send_mail("confirm mail", "進入此連結驗證:http://127.0.0.1:8000/main/resetconfirm?k=%s" % reset_complete_key2,
                #           "kevinliang1018@gmail.com", [user.email])
                send_mail("confirm mail", "進入此連結驗證:https://findjob2022project.herokuapp.com/main/resetconfirm?k=%s" % reset_complete_key2,
                          "kevinliang1018@gmail.com", [user.email])
                time.sleep(3)
                return HttpResponse("請置信箱驗證!")
        except:
            messages.add_message(
                request, messages.INFO, '非預期錯誤!')
            return render(request, 'reset.html')
    else:
        return render(request, 'reset.html')


def index(request):
    try:
        status = request.session['status']
        return render(request, 'index.html', context={'status': status})
    except:
        return render(request, 'index.html')


def joblist(request):
    return render(request, 'searchjob.html')


def company_signIn(request):
    if request.method == 'POST':
        companyname = request.POST['companyname']
        pid = request.POST['pid']
        email = request.POST['email']
        passwd = request.POST['passwd']
        try:
            try:
                companyacc.objects.get(pid=pid)
            except:
                companyacc.objects.get(email=email)
            account_exist = 0
        except:
            account_exist = 1

        if account_exist:
            if '' in [companyname, pid, email, passwd]:
                messages.add_message(
                    request, messages.INFO, '資料不完整請重新輸入!')
                return render(request, 'company_signIn.html')
            elif None == re.search(r"\w+@\w+\.\w+", str(email)):
                messages.add_message(
                    request, messages.INFO, '信箱格式錯誤請重新輸入!')
                return render(request, 'company_signIn.html')
            else:
                global com_complete_key
                global com_complete_key2
                global com_complete
                com_complete_key2 = com_complete_key
                companyname = str(companyname)
                pid = str(pid)
                email = str(email)
                passwd = str(passwd)
                com_complete = [companyname, pid, email, passwd]
                # send_mail("confirm mail", "進入此連結驗證:http://127.0.0.1:8000/main/company_confirm?k=%s" % com_complete_key2,
                #           "kevinliang1018@gmail.com", [email])
                send_mail("confirm mail", "進入此連結驗證:https://findjob2022project.herokuapp.com/main/company_confirm?k=%s" % com_complete_key2,
                          "kevinliang1018@gmail.com", [email])
                time.sleep(3)
                return HttpResponse('請至信箱驗證')
        else:
            messages.add_message(
                request, messages.INFO, '身分證或email已註冊過!')
            return render(request, 'company_signIn.html')
    else:
        return render(request, 'company_signIn.html')


def company_confirm(request):
    global com_complete
    global com_complete_key2
    try:
        if request.GET.get('k') == com_complete_key2:
            company = companyacc(
                companyname=com_complete[0],
                pid=com_complete[1],
                email=com_complete[2],
                passwd=com_complete[3]
            )

            company.save()
            messages.add_message(
                request, messages.INFO, '註冊成功')
            return redirect('login')
        else:
            messages.add_message(
                request, messages.INFO, '驗證錯誤，請重新註冊!')
            return redirect('company_signIn')
    except:
        messages.add_message(
            request, messages.INFO, '帳號已驗證過!')
        return redirect('company_signIn')


def companyjobs_edit(request):
    try:
        account = request.session['account']
        try:
            company = companyacc.objects.get(pid=account)
        except:
            company = companyacc.objects.get(email=account)
        pid = company.pid
        email = company.email
        jobslist = {pid+"_1": "職缺一", pid+"_2": "職缺二", pid +
                    "_3": "職缺三", pid+"_4": "職缺四", pid+"_5": "職缺五"}
        jobs_info = ["", company.companyname,
                     "", "", "", "", "", "", email, ""]
    except:
        messages.add_message(request, messages.INFO, '請進行登入!')
        return redirect('index')
    if request.method == 'POST':
        jobs_number = pid + "_" + request.POST['number']
        try:
            jobs = companyacc_jobs.objects.get(number=jobs_number)
            jobs_exist = 1
        except:
            jobs_exist = 0
        if jobs_exist:
            jobs_info[0] = jobs.number
            jobs_info[2] = jobs.title
            jobs_info[3] = jobs.uploaddate
            jobs_info[4] = jobs.content
            jobs_info[5] = jobs.require
            jobs_info[6] = jobs.salary
            jobs_info[7] = jobs.benefits
            jobs_info[9] = jobs.address
        else:
            jobs_info[0] = jobs_number
        return render(request, "company_jobs.html", {"jobs_info": jobs_info, "jobslist": jobslist[jobs_number]})
    else:
        jobs_number = pid+"_1"
        try:
            jobs = companyacc_jobs.objects.get(number=jobs_number)
            jobs_info[0] = jobs.number
            jobs_info[2] = jobs.title
            jobs_info[3] = jobs.uploaddate
            jobs_info[4] = jobs.content
            jobs_info[5] = jobs.require
            jobs_info[6] = jobs.salary
            jobs_info[7] = jobs.benefits
            jobs_info[9] = jobs.address
        except:
            pass
        return render(request, "company_jobs.html", {"jobs_info": jobs_info, "jobslist": jobslist[jobs_number]})


def companyjobs_save(request):
    if request.method == 'POST':
        account = request.session['account']
        try:
            company = companyacc.objects.get(pid=account)
        except:
            company = companyacc.objects.get(email=account)
        pid = company.pid
        jobs_number = request.POST['number']
        if '' in [jobs_number]:
            jobs_number = pid+"_1"
        jobslist = {pid+"_1": "職缺一", pid+"_2": "職缺二", pid +
                    "_3": "職缺三", pid+"_4": "職缺四", pid+"_5": "職缺五"}
        try:
            companyacc_jobs.objects.get(number=jobs_number)
            account_exist = 1
        except:
            account_exist = 0
        if account_exist == 0:
            jobs = companyacc_jobs()
        else:
            jobs = companyacc_jobs.objects.get(number=jobs_number)
        jobs.number = jobs_number
        time = datetime.datetime.now().date()
        jobs.companyname = company.companyname
        jobs.title = request.POST['title']
        jobs.uploaddate = time
        jobs.content = request.POST['content']
        jobs.require = request.POST['require']
        jobs.salary = request.POST['salary']
        jobs.benefits = request.POST['benefits']
        jobs.email = company.email
        jobs.address = request.POST['address']
        jobs.save()
        jobs_info = [jobs.number, jobs.companyname, jobs.title, jobs.uploaddate,
                     jobs.content, jobs.require, jobs.salary, jobs.benefits, jobs.email, jobs.address]
        messages.add_message(
            request, messages.INFO, 'Saved at %s' % time)
        return render(request, "company_jobs.html", {"jobs_info": jobs_info, "jobslist": jobslist[jobs_number]})
    else:
        return redirect("companyjobs_edit")


def partnerjobs(request):
    jobslist = companyacc_jobs.objects.all()
    jobs_info = []
    for jobs in jobslist:
        if '' in [jobs.number, jobs.companyname, jobs.title, jobs.uploaddate, jobs.content, jobs.require, jobs.salary, jobs.benefits, jobs.email, jobs.address]:
            continue
        else:
            jobs_info.append([jobs.number, jobs.companyname, jobs.title, jobs.uploaddate,
                             jobs.content, jobs.require, jobs.salary, jobs.benefits, jobs.email, jobs.address])
    if request.method == 'POST':
        return render(request, "partnerjobs.html", {"jobs_info": jobs_info})
    else:
        return render(request, "partnerjobs.html", {"jobs_info": jobs_info})
