from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
import uuid


class Common(models.Model):
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    is_deleted  = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)
    class Meta:
        abstract = True

def generateToken(user):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    return token
