from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .serializers import (UserRegistrationSerializer,ForgotAccountValidationSerializer)
from .functions.jwtToken import jwtToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.utils.common import generateToken
from core.utils.mailScheduler import scheduler
from django.utils import timezone
from django.conf import settings

        
class UserRegisterView(viewsets.ViewSet):
    serializers_class = UserRegistrationSerializer
    def post(self,request):
        context = {}
        try:
            payLoad = request.data
            serializer = self.serializers_class(data=payLoad)
            if not serializer.is_valid():
                context["status"]       = False
                context["status_code"]  = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            token = generateToken(user)
            user.token = token
            user.save()

            context["status"]       = True
            context['email']             = user.email
            context["status_code"]  = status.HTTP_200_OK
            context["message"]      = 'success'
            return Response(context, status=status.HTTP_200_OK) 
        except Exception as e:
            context["status"] = False
            context["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"] = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UserLoginView(viewsets.ViewSet):
    def post(self, request):
        context = {}
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user  = serializer.validated_data.get('user')
                authToken = jwtToken(user)
                context["token"]        = authToken
                context["status"]       = True
                context["status_code"]  = status.HTTP_200_OK
                context["message"]      = 'success'
                return Response(context, status=status.HTTP_200_OK)
            data = {'code':status.HTTP_400_BAD_REQUEST,'message':'error','data':serializer.errors}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {'code':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             
class ProfileView(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]
    def patch(self,request):
        context = {}
        try:
            user = request.user
            serializer = UserProfileSerializer(instance=user, data=request.data, partial=True)
            if not serializer.is_valid():
                context["status"]       = False
                context["status_code"]  = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            context["data"]      = serializer.data
            context["status"]       = True
            context["status_code"]  = status.HTTP_200_OK
            context["message"]      = 'success'
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            data = {'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)}
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self,request):
        context = {}
        try:
            user = request.user
            serializer = UserProfileSerializer(user)
            context["data"]      = serializer.data
            context["status"]       = True
            context["status_code"]  = status.HTTP_200_OK
            context["message"]      = 'success'
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            data = {'code':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class ForgetResetPassword(viewsets.ViewSet):
    serializers_class = ForgotAccountValidationSerializer
    def get(self,request):
        context = {}
        try:
            payload = request.GET
            serializer = self.serializers_class(data=payload)
            if not serializer.is_valid():
                context["status"]       = False
                context["status_code"]  = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.validated_data.get('user')
            token = serializer.validated_data.get('token')
            
            context["status"]       = True
            context["status_code"]  = status.HTTP_200_OK
            context["message"]      = 'success'
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            data = {'code':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        context = {}
        try:
            serializers_class   = ResetPasswordSerializer
            payload             = request.data
            serializer_          = serializers_class(data=payload)
            if not serializer_.is_valid():
                context["status"]       = False
                context["status_code"]  = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer_.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer_.validated_data.get('user')
            authToken = jwtToken(user)
            context["token"]        = authToken
            context["status"]       = True
            context["status_code"]  = status.HTTP_200_OK
            context["message"]      = 'success'
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            data = {'code':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)