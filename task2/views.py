from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from .models import Profile
import random

import http.client

from django.conf import settings
from django.contrib.auth import authenticate, login


# Create your views here.


def send_otp(phone_number, otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = {'content-type': "application/json"}
    url = "http://control.msg91.com/api/sendotp.php?otp=" + otp + "&message=" + "Your otp is" + otp + "&phone_number=" + phone_number + "&authkey=" + authkey + "&country=91"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None



def login_attempt(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')

        user = Profile.objects.filter(phone_number=phone_number, otp=otp).first()

        if user is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'login.html', context)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(phone_number, otp)
        request.session['phone_number'] = phone_number
        return redirect('login_otp')
    return render(request, 'login.html')


def login_otp(request):
    phone_number = request.session.has_key('phone_number')
    context = {'phone_number': phone_number}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(phone_number=phone_number, otp=otp).first()

        if otp == profile.otp:
            user = User.objects.get(id=profile.user.id)
            login(request, user)
            return redirect('dashboard')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'phone_number': phone_number}
            return render(request, 'login_otp.html', context)

    return render(request, 'login_otp.html', context)


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')

        user = User.objects.filter(email=email, first_name=first_name, last_name=last_name).first()
        profile = Profile.objects.filter(gender=gender, phone_number=phone_number).first()

        if user or profile:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'register.html', context)

        user = User(email=email, first_name=first_name, last_name=last_name)
        user.save()
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, gender=gender, phone_number=phone_number)
        profile.save()
        send_otp(phone_number, otp)
        request.session['phone_number'] = phone_number
        return redirect('otp')
    return render(request, 'register.html')


def otp(request):
    phone_number = request.session['phone_number']
    context = {'phone_number': phone_number}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(phone_number=phone_number, otp=otp).first()

        if otp == profile.otp:
            return redirect('dashboard')
        else:
            print('Wrong')

            context = {'message': 'Wrong OTP', 'class': 'danger', 'phone_number': phone_number}
            return render(request, 'otp.html', context)

    return render(request, 'otp.html', context)

def dashboard(request):

    return render(request,'dashboard.html')