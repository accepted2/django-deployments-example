from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import resolve,reverse
from django.contrib.auth.decorators import login_required

def index(request):
    context_dict ={'text': "hello world",'number': 100}
    return render(request,'basic_app/index.html',context_dict)
@login_required
def spicial(request):
    return HttpResponse("You are logges in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def register(request):

    registered=False
    if request.method =="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(request.POST['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered =True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basic_app/registration.html',context={'user_form':user_form, 'profile_form':profile_form,'registered':registered})
# Create your views here.

def user_login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("YOu accaunt not Active")
        else:
            print("SOMEONE tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            HttpResponse(request, "Invalid login details supplied")
            messages.error(request,"Invalid login details supplied")
            return render(request,'basic_app/login.html')
    else:
        return render(request,'basic_app/login.html',{})