from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

def HomePage(request):
    return render(request, 'home.html')

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if passwords match
        if pass1 != pass2:
            return HttpResponse("Your password and Confirm password are not same !!")

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists. Please choose a different one.")

        # Check if email already exists (optional but good practice)
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered. Try logging in or use another email.")

        # Create user
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html')





def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request,'login.html')




def LogoutPage(request):
    logout(request)
    return redirect('login')