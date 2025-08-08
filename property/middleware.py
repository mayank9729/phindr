from django.http import HttpResponseForbidden
from customer.models import IPAddress

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.getClientIPAddress(request)

        blockedIPList = IPAddress.objects.filter(is_blocked=True).values_list('ip',flat=True)
        if ip  in  blockedIPList:
            return HttpResponseForbidden("Your IP address is blocked.")
        response = self.get_response(request)
        return response

    def getClientIPAddress(self, request):
        """Get client IP address from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')