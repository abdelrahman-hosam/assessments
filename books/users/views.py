from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import user_serializer , login_serializer
from .models import library_user
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = user_serializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            if not library_user.objects.filter(username= serializer.validated_data['username']).exists():
                user = serializer.create_user(serializer_data= serializer.validated_data)
                username = serializer.validated_data['username']
                refresh_token = RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                return Response({'success_message': 'user has been created successfully' , 'username':username, 'access_token': str(access_token) , 'refresh_token': str(refresh_token)} , status= status.HTTP_201_CREATED)
            else: 
                return Response({'failure_message':'user already exists'} , status= status.HTTP_400_BAD_REQUEST)
    return Response({'failure_message':'user was not created'} , status= status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        print('here')
        serializer =login_serializer(data= request.data)
        if serializer.is_valid(raise_exception= True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = get_object_or_404(library_user , username= username)
            if check_password(password , user.password):
                refresh_token = RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                return Response({'success_message':'user has successfully logged in' , 'user_id':user.id , 'access_token': str(access_token) , 'refresh_token': str(refresh_token)} , status= status.HTTP_200_OK)
            else: 
               return Response({'failure_message': 'we could not log you in password or username is incorrect'} , status= status.HTTP_400_BAD_REQUEST )
    return Response({'failure_message': 'we could not log you in or it is a get request'})