from django.db import models

from django.utils import timezone
# Create your models here.
from django.db import models

# Create your models here.
class User_details(models.Model):
    username=models.CharField(default="",blank=True,null=True,max_length=100)
    email=models.EmailField(default="",blank=True,null=True,max_length=50)
    password=models.CharField(default="",blank=True,null=True,max_length=20)
    
# Create your models here.
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author=models.ForeignKey('User_details',on_delete=models.CASCADE)
    author_name=models.CharField(max_length=100,default="dhruv")
    title=models.CharField(max_length=50)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True,blank=True, null=True)