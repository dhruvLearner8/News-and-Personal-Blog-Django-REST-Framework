from rest_framework import serializers
from .models import Post,User_details
class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = ['id','author','author_name','title','content','created_at']
