from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import library_user
from books_n_authors.models import books
class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = library_user
        fields = ['username' , 'password']
    def create_user(self , serializer_data):
        username = serializer_data['username']
        password = serializer_data['password']
        hashed_password = make_password(password)
        new_user = library_user(username= username , password= hashed_password)
        new_user.save()
        return new_user
class login_serializer(serializers.Serializer):
    username = serializers.CharField(max_length = 250)
    password = serializers.CharField(write_only = True)
