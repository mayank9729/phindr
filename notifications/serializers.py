# notifications/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification, UserNotification

User = get_user_model()

class NotificationCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )
    send_to_all = serializers.BooleanField(default=False)

    def validate(self, data):
        if not data.get('send_to_all') and not data.get('user_ids'):
            raise serializers.ValidationError("Provide user_ids or set send_to_all=True")
        return data


class UserNotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="notification.id")
    title = serializers.CharField(source="notification.title")
    message = serializers.CharField(source="notification.message")
    seen = serializers.BooleanField()
    seen_at = serializers.DateTimeField(allow_null=True)

class NotificationSeenSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField()

    def validate_notification_id(self, value):
        request = self.context["request"]
        if not UserNotification.objects.filter(user=request.user, notification_id=value).exists():
            raise serializers.ValidationError("Notification not found for this user.")
        return value