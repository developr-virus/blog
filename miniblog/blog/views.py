from django.shortcuts import render,HttpResponseRedirect
from .forms import signupform,Loginform,Postform
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
def home(request):
    posts=Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts,'id1':'active'})

def about(request):
    return render(request, 'blog/about.html',{'id2':'active'})
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps,'id5':'active'})
    else:
        return HttpResponseRedirect('/login/',{'id4':'active'})
def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/',{'id1':'active'})
def userlogin(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=Loginform(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user=authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged In')
                    return HttpResponseRedirect('/dashboard/',{'id5':'active'})
        else:
            form=Loginform()
        return render(request, 'blog/login.html',{'form':form,'id4':'active'})
    else:
        return HttpResponseRedirect('/dashboard/',{'id5':'active'})
   
def signup(request):
    if request.method == 'POST':
        form=signupform(request.POST)
        if form.is_valid():
            messages.success(request,"Congrats! You are now a member of our group")
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form=signupform()
    return render(request, 'blog/signup.html', {'form':form,'id3':'active'})

def addpost(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=Postform(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Post(title=title,desc=desc)
                pst.save()
                form=Postform()
                return HttpResponseRedirect('/dashboard/',{'id5':'active'})
        else:
            form=Postform()
        return render(request,'blog/addpost.html',{'form':form,'id5':'active'})
    else:
        return HttpResponseRedirect('/login/',{'id4':'active'})
def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            form=Postform(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/',{'id5':'active'})
        else:
            pi=Post.objects.get(pk=id)
            form=Postform(instance=pi)
        return render(request,"blog/updatepost.html",{'form':form,'id5':'active'})
    else:
        return HttpResponseRedirect('/login/',{'id4':'active'})
def deletepost(request,id):
    if request.user.is_authenticated:
        pi=Post.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/',{'id5':'active'})
    else:
        return HttpResponseRedirect('/login/',{'id4':'active'})
