from django.shortcuts import get_object_or_404,render, redirect, render
from .models import *
import json
from django.views.decorators import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.core.exceptions import *
import datetime

# Create your views here.
def home(request):
    if 'id' in request.session.keys():
        if request.session['type'] == 'student':
            studentname = Student.objects.get(email = request.session['id'])
            context = {
                'name': studentname.name
            }
            return render(request, 'studenthome.html', context)
        else:
            employeename = Employee.objects.get(email = request.session['id'])
            context = {
                'name': employeename.name
            }
            return render(request, 'employeehome.html')
    else:
        return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('emailid')
        print(email)
        password = request.POST.get('password')
        try: 
            Student.objects.get(email = email)
            student = UserProfile.objects.get(email = email)
            if student.check_pass(password):
                request.session['id'] = email
                request.session['type'] = 'student'
            return redirect('/')
        except: 
            try: 
                Employee.objects.get(email = email)
                employee = UserProfile.objects.get(email = email)
                if employee.check_pass(password):
                    request.session['id'] = email
                    request.session['type'] = 'employee'
                return redirect('/')
            except:
                messages.error(request, 'Username and/or Password is/are incorrect!')
                return redirect('/login')
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('emailid')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        try:
            Student.objects.get(email = email)
            try:
                UserProfile.objects.get(email = email)
                messages.error('An account with this email id already exists in the database!')
                return redirect('/signup')
            except:
                if pass1 == pass2:
                    user = UserProfile(email = email, password = pass1)
                    user.save()
                    return redirect('/')
                else:
                    messages.error('Passwords do not match!')
                    return redirect('/signup')
        except:
            try:
                Employee.objects.get(email = email)
                try:
                    UserProfile.objects.get(email = email)
                    messages.error('An account with this email id already exists in the database!')
                    return redirect('/signup')
                except:
                    if pass1 == pass2:
                        user = UserProfile(email = email, password = pass1)
                        user.save()
                        return redirect('/')
                    else:
                        messages.error('Passwords do not match!')
                        return redirect('/signup')
            except:
                messages.error('No such email id exists in our database!')
                return redirect('/signup')
    else:
        return render(request, 'signup.html')

def 
