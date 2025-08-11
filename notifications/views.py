from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserNotification
from .serializers import NotificationCreateSerializer, UserNotificationSerializer, NotificationSeenSerializer

# Admin creates notification
class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def create(self, request):
        serializer = NotificationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Notification sent successfully"}, status=status.HTTP_201_CREATED)


# User views and marks notifications
class UserNotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        only_unseen = request.query_params.get("only_unseen","false").lower() == "true"
        
        if only_unseen:
            user_notification= UserNotification.objects.filter(user=request.user,seen=False)            
        else:
            user_notification = UserNotification.objects.filter(user=request.user)
        
        serializer=UserNotificationSerializer(user_notification,many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            user_notification = UserNotification.objects.get(user=request.user, notification_id=pk)
        except UserNotification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSeenSerializer(
            user_notification,
            data={"notification_id": pk},
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Notification marked as seen"})
