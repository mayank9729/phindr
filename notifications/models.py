# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        unique_together = ('user', 'notification')  # prevent duplicates
