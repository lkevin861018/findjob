# from asyncio.windows_events import NULL
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from main.models import Dreamreal, user_resume
from django.core.mail import send_mail
import re
import string
import random
import datetime
# Create your views here.

complete = []
complete_key = ''.join(random.choice(string.ascii_letters + string.digits)
                       for _ in range(10))
reset_complete = []
reset_complete_key = ''.join(random.choice(string.ascii_letters + string.digits)
                             for _ in range(12))


def confirm(request):
    global complete_key
    try:
        if request.GET.get('k') == complete_key:
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
            return render(request, 'signIn.html')
    except:
        messages.add_message(
            request, messages.INFO, '帳號已驗證過!')
        return render(request, 'signIn.html')


def resetconfirm(request):
    global reset_complete
    global reset_complete_key
    try:
        if request.GET.get('k') == reset_complete_key:
            user = Dreamreal.objects.get(email=reset_complete[0])
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
                lastname = str(lastname)
                firstname = str(firstname)
                pid = str(pid)
                email = str(email)
                passwd = str(passwd)
                # send_mail("confirm mail", "進入此連結驗證:http://127.0.0.1:8000/main/confirm?k=%s" % complete_key,
                #           "kevinliang1018@gmail.com", [email])
                send_mail("confirm mail", "進入此連結驗證:https://findjob2022project.herokuapp.com/main/confirm?k=%s" % complete_key,
                          "kevinliang1018@gmail.com", [email])
                global complete
                complete = [lastname, firstname, pid, email, passwd]

                return HttpResponse('請至信箱驗證')
        else:
            messages.add_message(
                request, messages.INFO, '身分證或email已註冊過!')
            return render(request, 'signIn.html')
    else:
        return render(request, 'signIn.html')


def login(request):
    try:
        if 'account' in request.session:
            account = request.session['account']
            passwd = request.session['passwd']
            try:
                user = Dreamreal.objects.get(pid=account)
            except:
                user = Dreamreal.objects.get(email=account)
            if passwd == user.passwd:
                return render(request, 'main.html')
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
                user = Dreamreal.objects.get(pid=account)
                request.session['account'] = user.pid
            except:
                user = Dreamreal.objects.get(email=account)
                request.session['account'] = user.email

            if user.passwd == passwd:
                request.session['passwd'] = user.passwd
                return render(request, 'main.html')
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
        del request.session['account']
        del request.session['passwd']
    except:
        pass
    return redirect("login")


def reset(request):
    if request.method == 'POST':
        global reset_complete
        global reset_complete_key
        account = request.POST['account']
        re_pass = request.POST['repass']
        chech_pass = request.POST['checkpass']
        try:
            user = Dreamreal.objects.get(pid=account)
        except:
            user = Dreamreal.objects.get(email=account)

        try:
            if user.passwd == re_pass:
                messages.add_message(
                    request, messages.INFO, '不可與原密碼相同!')
                return render(request, 'reset.html')
            elif '' in re_pass:
                messages.add_message(
                    request, messages.INFO, '密碼不可空白!')
                return render(request, 'reset.html')
            elif re_pass != chech_pass:
                messages.add_message(
                    request, messages.INFO, '密碼確認錯誤，請重新確認!')
                return render(request, 'reset.html')
            else:
                reset_complete = [user.email, re_pass]
                # send_mail("confirm mail", "進入此連結驗證:http://127.0.0.1:8000/main/resetconfirm?k=%s" % reset_complete_key,
                #           "kevinliang1018@gmail.com", [user.email])
                send_mail("confirm mail", "進入此連結驗證:https://findjob2022project.herokuapp.com/main/resetconfirm?k=%s" % reset_complete_key,
                          "kevinliang1018@gmail.com", [user.email])
                return HttpResponse("請置信箱驗證!")
        except:
            messages.add_message(
                request, messages.INFO, '非預期錯誤!')
            return render(request, 'reset.html')
    else:
        return render(request, 'reset.html')


def index(request):
    return render(request, 'index.html')
