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
    room_code=id
    username=request.session['username']
    return render(request,"chatapp/index.html",{'room_code':room_code,'username':username})

def home(request):
    return render(request,"chatapp/home.html")

def create_new(request):
    if request.method=='POST' and request.POST['username']!='':
        res = str(''.join(random.choices(string.ascii_letters, k=8)))
        while Room.objects.filter(room_code=res).count()!=0:
            res = str(''.join(random.choices(string.ascii_letters, k=8)))
        request.session['username']=request.POST['username']
        
        return  redirect('chatapp:index', id=res) 
    return render(request,"chatapp/home.html")

def join(request):
    print(request.POST['username'] , request.POST['room_id'])
    if request.method=='POST' and request.POST['username']!='' and request.POST['room_id']!='':
        request.session['username']=request.POST['username']
        return  redirect('chatapp:index', id=request.POST['room_id'])
    return render(request,"chatapp/home.html")
        

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
    
    logout(request)
    return redirect("chatapp:login")

    
