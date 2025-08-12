from django.contrib import admin
from .models import Notification,UserNotification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id','title']
admin.site.register(Notification,NotificationAdmin)

class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['id','seen']
admin.site.register(UserNotification, UserNotificationAdmin)
