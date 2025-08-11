from django.urls import path
from .views import NotificationViewSet, UserNotificationViewSet

notification_create = NotificationViewSet.as_view({'post': 'create'})
user_notifications_list = UserNotificationViewSet.as_view({'get': 'list'})
user_notifications_update = UserNotificationViewSet.as_view({'put': 'update'})

urlpatterns = [
    path('notifications/', notification_create),
    path('my/notifications/', user_notifications_list),
    path('my/notifications/<int:pk>/', user_notifications_update),
]
