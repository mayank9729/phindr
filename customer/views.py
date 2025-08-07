from .serializers import *
from .models import *
from core.utils.permissions import IsBuyer,IsAdmin
from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.utils.response_handler import ResponseHandler
from core.utils.common import generateToken
from .functions.jwtToken import jwtToken
from core.utils.random import hash_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# ✅ for admin view only
class AdminUserListView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    # GET /api/admin/users/?role=customer&is_active=true
    def list(self, request):
        try:
            users = User.objects.all()

            # Optional filters
            role = request.GET.get('role')
            is_active = request.GET.get('is_active')

            if role:
                users = users.filter(role=role)
            if is_active is not None:
                users = users.filter(is_active=is_active.lower() == 'true')

            serializer = AdminUserUpdateSerializer(users, many=True)
            return ResponseHandler.success(data=serializer.data)
        except Exception as e:
            return ResponseHandler.error(message="Failed to fetch users", status_code=500)

    # PATCH /api/admin/users/<user_id>/
    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)
            if not serializer.is_valid():
                return ResponseHandler.error(
                    message="Validation failed",
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return ResponseHandler.success(data=serializer.data)
        except User.DoesNotExist:
            return ResponseHandler.error(message="User not found", status_code=404)
        except Exception as e:
            return ResponseHandler.error(message="Update failed", status_code=500)

    # DELETE /api/admin/users/<user_id>/
    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            if user.role == 'admin':
                return ResponseHandler.error(message="Can delete admin", status_code=400)
            user.is_active = False
            user.save()
            return ResponseHandler.success(message="User deactivated")
        except User.DoesNotExist:
            return ResponseHandler.error(message="User not found", status_code=404)
        except Exception as e:
            return ResponseHandler.error(message="Deactivation failed", status_code=500)

# ✅ User Registration
class UserRegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return ResponseHandler.error(
                    message="Validation failed",
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            user = serializer.save()
            token = generateToken(user)
            user.token = token
            user.save()

            return ResponseHandler.success(data =
                                           {"email": user.email,
                                            "token": token,
                                            "first name" : user.first_name,
                                            "last name" : user.last_name,
                                            }
                                           )

        except Exception as e:
            return ResponseHandler.error(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ User Login
class UserLoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data.get('user')
                tokens = jwtToken(user)

                data = {
                    "refresh": tokens["refresh"],
                    "access": tokens["access"],
                    "email": user.email,
                    "name": f"{user.first_name} {user.last_name}",
                    "role": user.role
                }
                return ResponseHandler.success(data=data)

            return ResponseHandler.error(
                message="Invalid credentials",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return ResponseHandler.error(message="Login failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Profile View
class ProfileView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request):
        
        permission_classes = [IsAuthenticated, IsBuyer]
        try:
            serializer = UserProfileSerializer(request.user)
            return ResponseHandler.success(data=serializer.data)

        except Exception as e:
            return ResponseHandler.error(message="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        permission_classes = [IsAuthenticated, IsBuyer] 
     
        try:
            serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=True)
            if not serializer.is_valid():
                return ResponseHandler.error(
                    message="Validation failed",
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            instance=serializer.save()
            updated_serializer = UserProfileSerializer(instance)
            return ResponseHandler.success(data=updated_serializer.data)

        except Exception as e:
            return ResponseHandler.error(message="Update failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Forgot / Reset Password
class ForgetResetPassword(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = ForgotAccountValidationSerializer

    def get(self, request):
        try:
            serializer = self.serializer_class(data=request.GET)
            if not serializer.is_valid():
                return ResponseHandler.error(
                    message="Validation failed",
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            token = serializer.validated_data.get('token')
            return ResponseHandler.success(data={"token": token})

        except Exception as e:
            return ResponseHandler.error(message="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return ResponseHandler.error(
                    message="Validation failed",
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            user = serializer.validated_data.get('user')
            tokens = jwtToken(user)

            return ResponseHandler.success(data={
                "access": tokens["access"],
                "refresh": tokens["refresh"]
            })

        except Exception as e:
            return ResponseHandler.error(message="Reset failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ for the google auth
class AuthViewSet(viewsets.ViewSet):
     def post(self, request):
        serializer = TypeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        login_type = data["type"]
        email = data["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.create_user(
                email=email,
                password=hash_password
            )


        refresh = jwtToken(user)

        return ResponseHandler.success(data={
            "refresh": refresh["refresh"],
            "access": refresh["access"],
            "email"  : user.email,
            "name": f"{user.first_name.capitalize() or ""} {user.last_name or ""}".strip() or "guest",
            "role": user.role
            })
        
