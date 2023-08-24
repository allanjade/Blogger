import dataclasses
from email import message
from multiprocessing import context
from unicodedata import category
from winreg import QueryValue
from wsgiref.simple_server import demo_app
from django.shortcuts import render, redirect

from .models import User
 
from django.http import HttpResponse, request

from datetime import datetime,timedelta, date

from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import calendar

from .forms import UserSignup, UserLoginForm ,NewpostForm , ProfileForm
from django.template import loader
from django.contrib import messages
from django.utils.timezone import utc

from django.urls import reverse

# login required decorator
from django.contrib.auth.decorators import login_required

from django.views.generic.list import ListView
from django.utils.safestring import mark_safe
# filter data
from django.db.models import Q, Count
# for printint database data

# from .utils import render_to_pdf

from .models import *
# from .calendar_dep import Calendark

from django.db.models.signals import post_delete


# Create your views here.


def home(request):

    lastthree = BlogPost.objects.order_by('-created')[:3]

    recent = BlogPost.objects.order_by('-created')[:1]

    allposts = BlogPost.objects.order_by('-created')[:15]

    context = {'lastthree':lastthree, 'recent':recent, 'allposts':allposts}
    return render(request, 'base/home.html', context) 

def register(request):
    page = 'register'
    userform = UserSignup()
    user = User()
    countadmins = User.objects.filter(user_type='admin').count()
    if  request.method == 'POST':
        
        
        instance = User(user_type=request.POST.get('user_type'))
        userform = UserSignup(request.POST or None, instance=instance)

        if userform.is_valid():
            userform.save()
            messages.success(request, 'Account created successfully')
            return redirect('signin')
        else:
            messages.error(request, 'Error occurred created account')

    context = {'registerform':userform, 'page':page, 'admins':countadmins}
        
    return render(request, 'base/user.html', context)


def signin(request):
    page = 'login'
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.user_type == 'admin':
                        return redirect('admin')
                    elif user.user_type == 'visitor':
                        return redirect('home')
                else:
                    messages.error(request, 'Oops, this account has been disabled. Please contact your admin for assistance.')
            else:
                messages.error(request, 'Invalid credentials')
    
    else:
        form = UserLoginForm()
    context = {'form': form, 'page':page}
    return render(request, 'base/user.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def admin(request):
    posts = BlogPost.objects.all()

    context = {'posts':posts}
    return render(request, 'base/admin.html', context)

def visitor(request):
    return render(request, 'base/visitor.html')

def about(request):
    return render(request, 'base/about.html')


@login_required
def postnew(request):
    if request.user.user_type == 'admin':
        if request.method == 'POST':
            # Handle form submission and create a new blog post
            title = request.POST['title']
            description = request.POST['description']
            image = request.FILES.get('image')

            # Assuming you already have the user associated with the post
            poster = request.user

            blog_post = BlogPost.objects.create(
                poster=poster,
                title=title,
                description=description,
                image=image,
            )
      
            return redirect('admin')
        else:
            return render(request, 'base/post.html')
    else:
        return redirect('access_denied')  # You can define this view to display an access denied message.

def one_post(request, id):
    post_id = BlogPost.objects.get(id=id)

    context = {'postinfo':post_id}
    return render(request, 'base/single_post.html', context)


def post_update(request, id):
    postinstance = get_object_or_404(BlogPost, id=id)

    if request.user == postinstance.poster:  # Check if the user is the owner of the post
        if request.method == 'POST':
            form = NewpostForm(request.POST or None, request.FILES, instance=postinstance)  # Pass 'instance' to the form constructor
            if form.is_valid():
                form.save()
                return redirect('one_post', id=id)  # Redirect to the post's detail view
        else:
            form = NewpostForm(instance=postinstance)  # Pass 'instance' to the form constructor
        return render(request, 'base/post_edit.html', {'form': form, 'postdata':postinstance})
    else:
        return redirect('admin')  


def post_delete(request, id):
    post = get_object_or_404(BlogPost, id=id)

    if request.user == post.poster:  # Check if the user is the owner of the post
        if request.method == 'POST':
            post.delete()
            return redirect('admin')  # Redirect to the list of posts after deletion
        return render(request, 'base/post_delete.html', {'post': post})
    else:
        return redirect('access_denied')  # You can define this view to display an access denied message.


def profile(request):
    countprofiles = Profile.objects.all().filter(user=request.user).count()
    profileinfo = get_object_or_404(Profile, user_id = request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        username = request.user.id
        
        if form.is_valid():
            formdata = form.save(commit=False)
            formdata.user_id = username
            form.save()
            return redirect('home')  # Redirect to home or desired page
    else:
        form = ProfileForm()
    context = {'form': form, 'countprofiles': countprofiles, 'userdata':profileinfo}
    return render(request, 'base/profile/profile.html', context)
@login_required
def updateprofile(request, id):
    blogger = get_object_or_404(Profile, id=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=blogger)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=blogger)
    return render(request, 'base/profile/updateprofile.html', {'form': form})
@login_required
def deleteprofile(request, id):
    blogger = get_object_or_404(Profile, id=id)
    if request.method == 'POST':
        blogger.delete()
        return redirect('home')  # Redirect to home  page
    return render(request, 'base/profile/deleteprofile', {'blogger': blogger})
