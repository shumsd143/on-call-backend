from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,LoginSerializer
from django.contrib import auth
import jwt
from rest_framework import status
from on_call_medical import settings
from .models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
import json

# Create your views here.

class RegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes= (IsAuthenticated,)
    def post(self, request):
        if(request.user.is_admin):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                password=make_password(serializer.validated_data['password'])
                serializer.save(password=password)
                return Response({'detail': 'User successfully created'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'User is not authorized to create new user'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(email=username, password=password)
        if not user:
            try:
                user_by_phone=User.objects.get(phone=username)
                user = auth.authenticate(email=user_by_phone.email, password=password)
            except User.DoesNotExist:
                pass
        if user:
            auth_token = jwt.encode(
                {'email': user.email}, settings.JWT_SECRET_KEY)
            data = {'token': auth_token}
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    permission_classes= (IsAuthenticated,)
    def get(self,request,fomat=None):
        user=request.user
        return Response({
            'email':user.email,
            'phone':user.phone.__str__(),
            'is_admin':user.is_admin,
            'is_staff':user.is_staff,
        })
