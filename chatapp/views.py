from django.shortcuts import render ,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Room
from django.urls import reverse
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
import string
import random

# Create your views here.
def index(request,id):
    if request.user.is_authenticated and id!='' and 'username' in request.session and request.session['username']!='':
        if Room.objects.filter(room_code=id).count()==0:
            return redirect('chatapp:home')
        room_code=id
        if request.session['status']>0:
            return redirect('chatapp:home')
        request.session['status']=1
        username=request.session['username']
        lang=Room.objects.get(room_code=id).lang
        return render(request,"chatapp/index.html",{'room_code':room_code,'username':username,'lang':lang})
    return redirect('chatapp:login')
def home(request):
    if 'username' in request.session:
      del request.session['username']
    if 'status' in request.session:
      del request.session['status']
    
    if request.user.is_authenticated:
       return render(request,"chatapp/home.html")
    return redirect('chatapp:login')
def create_new(request):
    if request.user.is_authenticated:
        if request.method=='POST' and request.POST['username']!='' and request.POST['lang']!='':
            res = str(''.join(random.choices(string.ascii_letters, k=8)))
            while Room.objects.filter(room_code=res).count()!=0:
                res = str(''.join(random.choices(string.ascii_letters, k=8)))
            Room(room_code=res,lang=request.POST['lang']).save()

            request.session['username']=request.POST['username']
            request.session['status']=0
            return  redirect('chatapp:index', id=res) 
        return render(request,"chatapp/home.html")
    return redirect('chatapp:login')

def join(request):
    if request.user.is_authenticated:
        if request.method=='POST' and request.POST['username']!='' and request.POST['room_id']!='':
            request.session['username']=request.POST['username']
            request.session['status']=0
            if Room.objects.filter(room_code=request.POST['room_id']).count()==1:
               return  redirect('chatapp:index', id=request.POST['room_id'])
        return render(request,"chatapp/home.html")
    return redirect('chatapp:login')

def register_request(request):
    if request.user.is_authenticated:
        return redirect("chatapp:home")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("chatapp:home")
    return render (request,"chatapp/register.html")

def login_request(request):
    if request.user.is_authenticated:
        return redirect("chatapp:home")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect("chatapp:home")
            else:
                pass
        else:
            pass
    return render(request,'chatapp/login.html')

def logout_request(request):
    if 'username' in request.session:
      del request.session['username']
    if 'status' in request.session:
      del request.session['status']
    
    logout(request)
    return redirect("chatapp:login")

    
