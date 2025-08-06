from django.urls import path
from .views import (UserRegisterView,UserLoginView,ProfileView,ForgetResetPassword,AdminUserListView,AuthViewSet )
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', UserRegisterView.as_view({"post":"post"}),name='signup'),
    path('signin/', UserLoginView.as_view({"post":"post"}),name='signin'),
    path('forgot-password/', ForgetResetPassword.as_view({"get":"get"}),name='forgot-password'),
    path('reset-password/', ForgetResetPassword.as_view({"post":"post"}),name='reset-password'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update-profile/', ProfileView.as_view({"patch":"patch"}), name='update-profile'),
    path('get-profile/', ProfileView.as_view({"get":"get"}), name='get-profile'),
    path('admin-view/', AdminUserListView.as_view({"get":"list"}), name='get'),
    path('admin-view/<int:pk>/', AdminUserListView.as_view({"patch":"partial_update","delete":"destroy"}), name='update-delete'),
    path('login/',AuthViewSet.as_view({"post":"post"}), name='social-login'),
]
