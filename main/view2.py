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

def resume_style(request):
    if request.method == 'POST':
        return render(request, 'resume_style.html')
    else:
        return render(request, 'resume_style.html')


def resume_edit(request):
    account = request.session['account']
    try:
        user = Dreamreal.objects.get(pid=account)
    except:
        user = Dreamreal.objects.get(email=account)
    pid = user.pid
    lastname = user.lastname
    firstname = user.firstname
    try:
        resume = user_resume.objects.get(pid=pid)
        user_education = resume.user_education
        user_experience = resume.user_experience
        user_skill = resume.user_skill
        user_selfintroduction = resume.user_selfintroduction
        resumestyle = resume.user_resumestyle
    except:
        user_education = "education"
        user_experience = "experience"
        user_skill = "skill"
        user_selfintroduction = "selfintroduction"
        resumestyle = "0"
    if request.method == 'POST':
        resumestyle = request.POST['style']
        return render(request, "resume_edit.html", {"resumestyle": resumestyle, "lastname": lastname, "firstname": firstname, "user_education": user_education, "user_experience": user_experience, "user_skill": user_skill, "user_selfintroduction": user_selfintroduction})
    else:
        return render(request, "resume_edit.html", {"resumestyle": resumestyle, "lastname": lastname, "firstname": firstname, "user_education": user_education, "user_experience": user_experience, "user_skill": user_skill, "user_selfintroduction": user_selfintroduction})


def resume_save(request):
    if request.method == 'POST':
        account = request.session['account']
        try:
            user = Dreamreal.objects.get(pid=account)
        except:
            user = Dreamreal.objects.get(email=account)
        pid = user.pid
        lastname = user.lastname
        firstname = user.firstname
        try:
            resume = user_resume.objects.get(pid=pid)
        except:
            resume = user_resume()
        resume.pid = pid
        resume.lastname = lastname
        resume.firstname = firstname
        resume.user_resumestyle = str(request.POST['user_resumestyle'])
        resume.user_skill = str(request.POST['user_skill'])
        resume.user_selfintroduction = str(
            request.POST['user_selfintroduction'])
        resume.user_education = str(request.POST['user_education'])
        resume.user_experience = str(request.POST['user_experience'])
        resume.save()
        time = datetime.datetime.now().ctime()
        messages.add_message(
            request, messages.INFO, 'Saved at %s' % time)
        return render(request, "resume_edit.html", {"resumestyle": resume.user_resumestyle, "lastname": resume.lastname, "firstname": resume.firstname, "user_education": resume.user_education, "user_experience": resume.user_experience, "user_skill": resume.user_skill, "user_selfintroduction": resume.user_selfintroduction})
    else:
        return render(request, "resume_edit.html")