from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import Notification, UserNotification

User = get_user_model()


class NotificationCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()
    to_all = serializers.BooleanField(default=False)
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    def validate(self, attrs):
        # अगर सभी को नहीं भेजनी और user_ids नहीं दिए → error
        if not attrs.get("to_all") and not attrs.get("user_ids"):
            raise serializers.ValidationError("Either set 'to_all' to true or provide 'user_ids'.")

        # अगर user_ids दिए हैं तो check करें कि सभी valid हों
        if attrs.get("user_ids"):
            db_users = User.objects.filter(id__in=attrs["user_ids"])
            if db_users.count() != len(attrs["user_ids"]):
                raise serializers.ValidationError("Some provided user IDs are invalid.")

        return attrs

    def create(self, validated_data):
        user_ids = validated_data.pop("user_ids", [])
        to_all = validated_data.get("to_all", False)

        # Main notification create
        notification = Notification.objects.create(**validated_data)

        # Target users निकालना
        if to_all:
            users = User.objects.all()
        else:
            users = User.objects.filter(id__in=user_ids)

        # Bulk create for performance
        UserNotification.objects.bulk_create(
            [UserNotification(user=user, notification=notification) for user in users]
        )

        return notification


class UserNotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="notification.id")
    title = serializers.CharField(source="notification.title")
    message = serializers.CharField(source="notification.message")
    seen = serializers.BooleanField()


class NotificationSeenSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField()

    def validate_notification_id(self, value):
        try:
            user_notification = UserNotification.objects.get(
                user=self.context["request"].user,
                notification_id=value
            )
        except UserNotification.DoesNotExist:
            raise serializers.ValidationError("Notification not found for this user.")

        if user_notification.seen:
            raise serializers.ValidationError("Notification already marked as seen.")

        return value

    def update(self, instance, validated_data):
        instance.seen = True
        instance.seen_at = datetime.now()
        instance.save()
        return instance
