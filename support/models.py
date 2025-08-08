from django.db import models
import uuid
from django.conf import settings
# Create your models here.

class SupportTicket(models.Model):
    QUERY_TYPES = [
        ('issue', 'Issue'),
        ('help', 'Help'),
        ('query', 'Query'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICE=[
        ('open','Open'),
        ('close','Close'),
    ]
    ticket_id = models.CharField(max_length=8,default=uuid.uuid4().hex[:6].upper())
    date = models.DateField(auto_now_add=True)
    reason = models.TextField(default=None)
    query_type = models.CharField(max_length=20,choices=QUERY_TYPES,default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=20,choices=STATUS_CHOICE,default='open')
    raised_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets_raised', on_delete=models.CASCADE)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets_closed', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.ticket_id} - {self.status}"