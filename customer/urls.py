from django.urls import path
from .views import (UserRegisterView,UserLoginView,ProfileView,ForgetResetPassword)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', UserRegisterView.as_view({"post":"post"}),name='signup'),
    path('signin/', UserLoginView.as_view({"post":"post"}),name='signin'),
    path('forgot-password/', ForgetResetPassword.as_view({"get":"get"}),name='forgot-password'),
    path('reset-password/', ForgetResetPassword.as_view({"post":"post"}),name='reset-password'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update-profile/', ProfileView.as_view({"patch":"patch"}), name='update-profile'),
    path('get-profile/', ProfileView.as_view({"get":"get"}), name='get-profile'),
]
