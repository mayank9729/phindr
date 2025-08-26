from django.contrib import admin
from .models import Notification,UserNotification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id','title',"created_at"]
admin.site.register(Notification,NotificationAdmin)

class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['id','seen','seen_at']
admin.site.register(UserNotification, UserNotificationAdmin)
