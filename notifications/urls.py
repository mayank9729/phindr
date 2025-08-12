# notifications/urls.py
from django.urls import path
from .views import NotificationViewSet

notification_list = NotificationViewSet.as_view({"get": "list", "post": "create"})
notification_mark_seen = NotificationViewSet.as_view({"patch": "partial_update"})
notification_mark_all = NotificationViewSet.as_view({"put": "update_all"})

urlpatterns = [
    path("notification/", notification_list, name="notification-list"),
    path("notification/<int:pk>/", notification_mark_seen, name="notification-mark-seen"),
    path("mark-all/", notification_mark_all, name="notification-mark-all"),
]
