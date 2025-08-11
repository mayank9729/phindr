from django.db import models
from django.conf import settings

class Notification(models.Model):
    title = models.CharField(max_length=255)              # Notification का title
    message = models.TextField()                          # Notification का content
    created_at = models.DateTimeField(auto_now_add=True)  # कब बनाई गई
    to_all = models.BooleanField(default=False)           # सभी users को भेजनी है या नहीं

    def __str__(self):
        return self.title


class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)             # user ने देखी या नहीं
    seen_at = models.DateTimeField(null=True, blank=True) # कब देखी

    def __str__(self):
        return f"{self.user} - {self.notification.title}"
