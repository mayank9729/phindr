from rest_framework import serializers
from .models import User,LicenceCode
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password,check_password
from core.utils.common import generateToken

class UserRegistrationSerializer(serializers.ModelSerializer):
    password    = serializers.CharField(required=True)
    first_name  = serializers.CharField(required=True)
    last_name   = serializers.CharField(required=False,allow_null=True, allow_blank=True)
    email       = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all(),message='Email already exists')])

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['is_active'] = True
        return super().create(validated_data)
    
    class Meta:
        model = User
        fields = ('id', 'email','phone', 'unique_id','password','first_name','last_name')
        extra_kwargs = {
            'password': {
                'required': True
            },
            'email': {
                'required': True
            },
            'first_name': {
                'required': True
            },
            'last_name': {
                'required': False
            }
        }

class UserLoginSerializer(serializers.Serializer):
    email       = serializers.EmailField(required=True)
    password    = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        email       = data.get('email')
        password    = data.get('password')
        if email and password:
            modelClass = self.Meta.model

            userObj = modelClass.objects.filter(email=email,is_active=False)
            if userObj.exists():
                raise serializers.ValidationError({'account_status':'Account is not verified'})

            userObj = modelClass.objects.filter(email=email)
            if not userObj.exists():
                raise serializers.ValidationError('Invalid credentials')
            
            savedPasswordHash = userObj.first().password
            if not check_password(password,savedPasswordHash):
                raise serializers.ValidationError('Invalid credentials')
            
            data['user'] = userObj.first()
        else:
            raise serializers.ValidationError('Must include "email" and "password"')
        return data
  
class UserProfileSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    email           = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','password', 'old_password', 'new_password')
        extra_kwargs = {
            'email': {'read_only': True},
            'password': {'write_only': True, 'required': False},
        }

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        if new_password and not old_password:
            raise serializers.ValidationError({"old_password": "This field is required to update the password."})
        if old_password and not new_password:
            raise serializers.ValidationError({"new_password": "This field is required to update the password."})
        if old_password and new_password:
            user = self.instance 
            if not check_password(old_password, user.password):
                raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        return attrs

    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password', None)
        new_password = validated_data.pop('new_password', None)

        if old_password and new_password:
            instance.set_password(new_password)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
       
class ForgotAccountValidationSerializer(serializers.Serializer):
    email    = serializers.CharField(required=True)
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            
            try:
                userObj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({"email": "Account not found"}) 

            userObj = User.objects.get(email=email)
            if not userObj.is_active:
                raise serializers.ValidationError({"email": "Account not activated"}) 
            token = generateToken(userObj)
            userObj.token = token
            userObj.save()
            attrs['user'] = userObj
            attrs['token'] = token
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Email is required"}) 
        return attrs
    
class ResetPasswordSerializer(serializers.Serializer):
    password    = serializers.CharField(required=True)
    token       = serializers.CharField(required=True)
    def validate(self, attrs):
        token = attrs.get('token')
        password = attrs.get('password')
        try:
            userObj = User.objects.get(token=token)
            userObj.password = make_password(password)
            userObj.token = ''
            userObj.save()
            attrs['user'] = userObj
        except User.DoesNotExist:
            raise serializers.ValidationError({"token": "token is expired"}) 
        return attrs
    