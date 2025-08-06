from django.http import HttpResponseForbidden
from .models import IPAddress

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.getClientIPAddress(request)
        print(f"Client IP: {ip}") 
        
        try:
            ip_record = IPAddress.objects.get(ip=ip)
            if not ip_record.is_active:
                return JsonResponse({'detail': 'Access denied. IP is inactive.'}, status=403)
        except IPAddress.DoesNotExist:
            return JsonResponse({'detail': 'Access denied. IP not recognized.'}, status=403)
        response = self.get_response(request)
        print("After view")

        return response

    def getClientIPAddress(self, request):
        """Get client IP address from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')