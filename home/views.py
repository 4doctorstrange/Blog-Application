from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import RegisterationForm, LoginForm, PostForm
from home.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post,Contact
from django.contrib.auth.models import Group,User

# Create your views here.


def index(request):
    posts = Post.objects.order_by('-date').all()

    return render(request, 'index.html', {'posts': posts})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        mesg = request.POST['message']
        ob = Contact(name=name, email=email, contact=contact, message=mesg)
        ob.save()
        messages.success(request, 'Your responses are successfully subitted!')

    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, "Conratulations! It's a pleasure to have you. Please login to continue ")
            user = form.save()
            return redirect('/login')
    else:
        form = RegisterationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=name, password=password)
                
                if user:
                    login(request, user)
                    return redirect('/dashboard')
                    
                else:
                    messages.info(request, 'Invalid credentials')
                    return render(request,"login.html")
            else:
                messages.info(request, 'Invalid credentials')
                return redirect('login')

        else:
            form = LoginForm
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('/dashboard')


def user_logout(request):
    logout(request)
    return redirect('/')


def dashboard(request):
    if request.user.is_authenticated:
        
        if request.user.username == 'Admin':
            user = request.user
            username = user.username
            posts = Post.objects.all()
            return render(request,'dashboard.html', {"posts":posts, 'username':username })

        else:
            posts = Post.objects.filter(author = request.user)
            user = request.user
            username=user.username
            return render(request, 'dashboard.html', {'posts': posts, 'username':username
                })
    else:
        messages.warning(request, "Looks like you are not logged in")
        return redirect('/login')

def view_profile(request, username):
    user = request.user
    if request.user.is_authenticated and user.username==username:
        print(user.username)
        username= user.username
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        date = user.date_joined
        posts = Post.objects.filter(author=user).count()
        

        return render(request, 'profile.html',{'first_name':first_name, 'last_name':last_name, 'username':username,'date':date,'email':email,'posts':posts} )

    elif request.user.is_authenticated and us.username==username:
        return redirect('/dashboard')

    else:
        return redirect('/login')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc, author = request.user)
                pst.save()
                messages.success(request, "Thanks for making a post!")
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'addpost.html', {'form': form})
    else:
        return redirect('/login')


def update_post(request, id):
    if request.user.is_authenticated and request.user.username!='Admin':
        if request.method == 'POST':
            instance=Post.objects.get(pk=id)
            pi = Post.objects.filter(id=id)[0]
            ids = Post.objects.filter(author=request.user)  #getting all the posts written by logged in user
            
            fl=0

            for i in ids:
                                     # comparing with all ids
                if i.id==pi.id:
                    fl=1
            if fl==1:            #only update when that post is written by logged in author
                form = PostForm(request.POST, instance=instance)
                if form.is_valid():
                    messages.success(request, "Post updated!")
                    form.save()
            else:
                return redirect('/dashboard')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'updatepost.html', {'form': form})

    elif request.user.username =='Admin':
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                messages.success(request, "Post updated!")
                form.save()
            else:
                return redirect('/dashboard')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'updatepost.html', {'form': form})

    else:
        messages.warning(request, "Please login to edit a post")
        return redirect('/login')


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            

        return redirect('/dashboard')
    else:
        messages.warning(request, "Please login to delete a post!")
        return redirect('/login')

def post(request,id):
    post = Post.objects.get(pk=id)
    return render(request,'post.html',{'post':post})