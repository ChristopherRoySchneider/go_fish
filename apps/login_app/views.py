from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from django import forms
from datetime import datetime
import bcrypt

def index(request):
    return render(request, 'login_app/index.html')

def login_display(request):
    return render(request, 'login_app/login_display.html')

def registration(request):
    return render(request, 'login_app/registration.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    request.session['first_name'] = request.POST['first-name']
    request.session['last_name']= request.POST['last-name']
    request.session['username']= request.POST['username']

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/registration')

    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name = request.POST['first-name'], last_name = request.POST['last-name'], username = request.POST['username'], password=hash1)
        user = User.objects.get(username=request.POST['username'])
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        return redirect('/gofish')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_display')
    else: 
        user = User.objects.get(username=request.POST['username'])
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        return redirect('/gofish')

def success(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            "name": user.first_name
        }
        return render(request, "login_app/success.html",context)
    else: 
        return redirect("/")
def logout(request):
    request.session.flush()
    
    return redirect("/")

def myaccount(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            "user": user
        }
        return render(request, "login_app/myaccount.html",context)
    else: 
        return redirect("/")

def update(request):
    errors = User.objects.basic_validator(request.POST)

    print(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect("/myaccount")
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.get(id=request.session['user_id'])
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.birthday = request.POST['birthday']
        user.email = request.POST['email']
        user.password=hash1 
        user.save()
        return redirect("/gofish")