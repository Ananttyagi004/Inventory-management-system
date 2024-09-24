import logging
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserRegisterSerializer, UserLoginSerializer

# Set up logging
logger = logging.getLogger('account')

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterUser(APIView):
    serializer_class=UserRegisterSerializer
    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            logger.info(f"New user registered: {user.username}")  
            return Response({'msg': 'User Created', 'token': token}, status=status.HTTP_201_CREATED)
        logger.error(f"Registration failed with errors: {serializer.errors}") 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    serializer_class=UserLoginSerializer
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                logger.info(f"User logged in: {username}")  
                return Response({'msg': 'Login Success!', 'token': token}, status=status.HTTP_200_OK)
            logger.warning(f"Failed login attempt for username: {username}")  
            return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Login failed with errors: {serializer.errors}")  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
