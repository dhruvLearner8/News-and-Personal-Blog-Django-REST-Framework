from django import http
from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from numpy import source
from .models import User_details,Post
from newsapi import NewsApiClient
from .serializers import PostSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import smtplib
import random
import email.message

# Create your views here.
def login(request):
    if request.method=='POST':
        pass1=request.POST['password']
        email=request.POST['email']
        if User_details.objects.filter(email=email).exists():
            obj1=User_details.objects.get(email=email)
            if obj1.password==pass1:
                request.session['blog_user']=obj1.id
                return redirect('home')
            else:
                messages.info(request,'Wrong Password')
                return redirect('login')
        else:
            messages.info(request,'wrong email entered')


    else:
        return render(request,'login.html')
# Create your views here.


def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        
        if User_details.objects.filter(username=username).exists():
            messages.info(request,'Username Already taken')
            print('username taken')
            return redirect('register')
        if User_details.objects.filter(email=email).exists():
            messages.info(request,'Email Already Taken')
            return redirect('register')
        if pass1!=pass2:
            messages.info(request,'Password not matching!!')
            return redirect('register')
        Lower=False
        Upper=False
        num=False
        
        if (pass1==pass2 and len(pass1)>=8):
            for i in pass1:
                if ord(i)>=65 and ord(i)<=91:
                    Upper=True
                    break
            for i in pass1:
                if ord(i)>=97 and ord(i)<=123:
                    Lower=True
                    break
            for i in pass1:
               # print(ord(i))
                if (ord(i)<65 or ord(i)>91) :
                    if (ord(i)<97 or ord(i)>123):
                        
                        num=True
                        break  
            
            #print(num,Upper,Lower)
            if (Lower is True and Upper is True and num is True):
                print(num)
                obj1=User_details()
                obj1.username=username
                obj1.email=email
                obj1.password=pass1
                obj1.save()
                return redirect('login')
            else:
                messages.info(request,'please check validation of your password')
                return redirect('register')
        else:
            messages.info(request,'Password must be atleast 8 character long')
            return redirect('register')


    else:
        return render(request,'register.html')

def home(request):
    if 'blog_user' in request.session.keys():
        newsApi= NewsApiClient(api_key='d687b68ba56942568fa4ce1153fbc9ea')
        headLines=newsApi.get_top_headlines(sources='bbc-news,business-insider,bbc-sport,cbc-news')
        articles=headLines['articles']
        desc=[]
        news=[]
        img=[]
        url=[]
        for i in range(0,len(articles)):
            article=articles[i]
            desc.append(article['description'])
            news.append(article['title'])
            img.append(article['urlToImage'])
            url.append(article['url'])
        mylist=zip(news,desc,img,url)
        return render(request,'home.html',context={'mylist':mylist})
    else:
        return redirect('login')

def dashboard(request):
    if 'blog_user' in request.session.keys():
        user=User_details.objects.get(id=int(request.session['blog_user']))
        blog=Post.objects.filter(author=user)
        
        return render(request,'dashboard.html',{'blog':blog,'user':user})


def createblog(request):
    if 'blog_user' in request.session.keys():
        if request.method=='POST':
            title=request.POST['title']
            content=request.POST['content']

            user=User_details.objects.get(id=int(request.session['blog_user']))
            #blog=Post.objects.filter(author=user)
            blog=Post()
            #blog.id=pk
            blog.author=user
            blog.author_name=user.username
            blog.title=title
            blog.content=content
            blog.save()
            return redirect('dashboard')
        else:
            return render(request,'createblog.html')
    else:
        return redirect('login')

def Delete_blog(request,id):
    if 'blog_user' in request.session.keys():  
        blog = Post.objects.get(id = id)
        blog.delete()
        return redirect('dashboard')
    else:
        return redirect('login')

def view(request,id):
    if 'blog_user' in request.session.keys():  
        blog = Post.objects.get(id = id)
        return render(request,'view.html',{'blog':blog})

    
def dash1(request):
    if 'blog_user' in request.session.keys():
        return redirect('http://127.0.0.1:8000/dashboard')

def home1(request):
    if 'blog_user' in request.session.keys():
        return redirect("http://127.0.0.1:8000/home")

def cr1(request):
    if 'blog_user' in request.session.keys():
        return redirect("http://127.0.0.1:8000/createblog")

@api_view(['GET','POST'])
def post_list(request, format=None):
    if request.method=='GET':
        posts=Post.objects.all()
        serializer= PostSerializers(posts,many=True)
        return Response(serializer.data)
       # return JsonResponse({"drinks":serializer.data})
    if request.method=='POST':
        serializer= PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def post_detail(request,id,format=None):
    try:
       post= Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=PostSerializers(post)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer=PostSerializers(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def logout(request):
    if 'blog_user' in request.session.keys():
        del request.session['blog_user']
        return redirect('login')
    else:
        return redirect('login')


'''def edit_blog(request,id):
    if 'blog_user' in request.session.keys():
        blog=Post.objects.filter(id=id)
        #form=Post(request.POST or None)
        return render(request,'edit.html',{blog:'blog'})'''

'''def save(request):
    if 'blog_user' in request.session.keys():
        if request.method=='POST':
            title=request.POST['title']
            content=request.POST['content']
            id=request.POST['postId']
            
            print(id)
            blog=Post.objects.filter(id=id)
            blog.title=title
            blog.content=content
            blog.save()
            return redirect('http://127.0.0.1:8000/dashboard')'''

