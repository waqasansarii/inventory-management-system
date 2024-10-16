from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status

from ..serializer import SignupSerializer,LoginSerializer
from ..permission import IsAdmin

@api_view(['POST'])
@permission_classes([IsAdmin])
def create_user(req:Request):
    data = req.data
    # print(req.user.is_superuser,req.user.email)
    serializer = SignupSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        User.objects.create(**serializer.validated_data)
        return Response(serializer.data,status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(req:Request):
    data = req.data
    print(req.user)
    
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        password= serializer.validated_data['password']
        username= serializer.validated_data['username']
        user = authenticate(req,username=username,password=password)
        if user is not None:
            login(req,user=user)
            return Response('login success',status.HTTP_200_OK)
        else:
            return Response('Invalid credentials',status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(req:Request):
    logout(request=req)
    return Response('Logout success',status.HTTP_200_OK)    
        