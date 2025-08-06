from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)

def log_permission_check(user, role_required, passed, view_name=None):
    logger.info(
        f"[PERMISSION CHECK] User: {user.email if user.is_authenticated else 'Anonymous'} | "
        f"Role Required: {role_required} | "
        f"User Role: {getattr(user, 'role', 'N/A')} | "
        f"View: {view_name} | "
        f"Result: {'GRANTED' if passed else 'DENIED'}"
    )

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role == 'admin'
        log_permission_check(request.user, 'admin', allowed, view.__class__.__name__)
        return allowed

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role == 'seller'
        log_permission_check(request.user, 'seller', allowed, view.__class__.__name__)
        return allowed

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        allowed = request.user.is_authenticated and request.user.role == 'buyer'
        log_permission_check(request.user, 'buyer', allowed, view.__class__.__name__)
        return allowed
