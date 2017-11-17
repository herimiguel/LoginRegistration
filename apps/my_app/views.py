from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    
    return render (request, 'my_app/index.html')

def registration_process(request):
    
    if request.method == "POST":
        user_name = request.POST['user_name']
        last_name = request.POST['last_name']
        email_name = request.POST['email_name']
        password = request.POST['password']

    # if request.method == "POST":
        isValid = True
        minValName = 2
        minValPass = 8

    if len(request.POST['user_name']) < minValName:
        messages.error(request, " Name must be at least 2 characters!")
        isValid = False        
                
        
    if len(request.POST['last_name']) < minValName:
        messages.error(request, "last name must be at least 2 characters!")   
        isValid = False       
        
    if len(request.POST['email_name']) < minValName:
        messages.error(request, "Email is required!")
        isValid = False        
        
    if  request.POST['email_name'] != email_name:
        messages.error(request, "This email is already registered!")
        isValid = False       
        

    if len(request.POST['password']) < minValPass:
        messages.error(request, "Password is required!")
        isValid = False        
         
        
    if request.POST['confirm-password'] != request.POST['password']:
        messages.error(request, "Password confirmation failed")
        isValid = False        
        

    if not isValid:
        return redirect('/')

    if request.POST['confirm-password'] == password:
       
        try:
            user= User.objects.create(user_name = user_name, last_name= last_name, email_name= email_name, password = password)
        except IntegrityError:
            messages.error(request, 'This Email is already registered!')
            return redirect ('/')
        request.session['user_id'] = user.id
    return redirect('/success')

def login_process(request):
    if request.method == "POST":
        email_name = request.POST['email_name']
        password = request.POST['password']
        isValid = True
        minVal = 2

    if len(request.POST['email_name']) < minVal:
        messages.error(request, "Email is required!")
        isValid = False

    if len(request.POST['password']) < minVal:
        messages.error(request, "password is required!")
        isValid = False

    try:
        User.objects.get(email_name= request.POST['email_name'], password= request.POST['password'])

    except ObjectDoesNotExist:
        messages.error(request, "email and password don't match")
        isValid = False
    else:
        messages.error(request, "YOU ARE NOW LOGGED IN!")
        
    if not isValid:
        return redirect('/')
    else:
        request.session['user_id']= (User.objects.get(email_name= request.POST['email_name'])).id
        
        return redirect('/success')

def success(request):
    if 'user_id' in request.session.keys():
        user= User.objects.get(id=request.session['user_id'])
    context={
        'user': user
    }
    return render(request, 'my_app/success.html', context)

def logout_user(request):
    request.session.clear()
    messages.success(request, "Successfully logged out")
    return redirect('/')
