from django.urls import path
from .views import SupportTicketViewSet

urlpatterns = [
    path('ticket/', SupportTicketViewSet.as_view({"get":"list_tickets"}),name='list_tickets'),
    path('ticket/create/', SupportTicketViewSet.as_view({"post":"create_ticket"}),name='create_ticket'),
    path('ticket/<int:pk>/status/', SupportTicketViewSet.as_view({"patch": "change_status"}),name='change_status'),
]
