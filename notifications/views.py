# notifications/views.py
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from core.utils.response_handler import ResponseHandler
from .models import Notification, UserNotification
from .serializers import (
    NotificationCreateSerializer,
    UserNotificationSerializer,
    NotificationSeenSerializer
)
from django.utils import timezone

User = get_user_model()

class NotificationViewSet(viewsets.ViewSet):
    """
    Admin can create notifications (to all or selected users)
    Users can list their notifications
    Users can mark seen/unseen
    """
    permission_classes = [IsAuthenticated]

    # List notifications for logged-in user
    def list(self, request):
        try:
            user = request.user
            seen_param = request.query_params.get("seen")
            user_notifications = (
                UserNotification.objects.filter(user=request.user)
                .select_related("notification")
                .order_by("-notification__created_at")
            )

            if seen_param is not None:
                if seen_param.lower() in ["true", "1"]:
                    user_notifications = user_notifications.filter(seen=True)
                elif seen_param.lower() in ["false", "0"]:
                    user_notifications = user_notifications.filter(seen=False)
                else:
                    return ResponseHandler.error(
                        message="Invalid value for 'seen'. Use true/false or 1/0.",
                        status_code=400
                    )

            serializer = UserNotificationSerializer(user_notifications, many=True)
            return ResponseHandler.success(
                data=serializer.data,
                message="success"
            )
        except Exception as e:
            return ResponseHandler.error(
                message="Something went wrong while fetching notifications",
                error=str(e),
                status_code=500
            )

    # Admin creates notification
    def create(self, request):
        if not request.user.is_staff:
            return ResponseHandler.error(message="You are not allowed to create notifications")

        serializer = NotificationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()  # Calls create()

        return ResponseHandler.success(
            data={
            "notification_id": notification.id,
            "title": notification.title,
            "message": notification.message
            },
        message="Notification created successfully")
    
    def partial_update(self, request, pk=None):
        try:
            user_notification = UserNotification.objects.get(
                user=request.user,
                notification_id=pk
            )
        except UserNotification.DoesNotExist:
            return ResponseHandler.error(
                message="Notification not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if user_notification.seen:
            return ResponseHandler.success(message="Notification already marked as seen")

        user_notification.seen = True
        user_notification.seen_at = timezone.now()
        user_notification.save()

        return ResponseHandler.success(message="Notification marked as seen")
    
    
            
    # Mark all as seen
    def update_all(self, request):
        user_notification=UserNotification.objects.filter(user=request.user, seen=False)
        
        if not user_notification.exists():
            return ResponseHandler.success(
                message="All notifications are already marked as seen"
            )
        
        user_notification.update(seen=True)
        return ResponseHandler.success(
            message="All notifications marked as seen"
        )
