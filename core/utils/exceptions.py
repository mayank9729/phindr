from rest_framework.views import exception_handler
from rest_framework import serializers

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(exc, serializers.ValidationError):
        # Customize error format
        error_messages = " ".join(
            [str(err) for errs in exc.detail.values() for err in errs]
        )
        response.data = {
            "status": "failure",
            "errors": error_messages
        }

    return response
