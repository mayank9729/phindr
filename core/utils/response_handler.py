from rest_framework.response import Response
from rest_framework import status as http_status

class ResponseHandler:
    @staticmethod
    def success(message="success", data=None, status_code=http_status.HTTP_200_OK):
        return Response({
            "status_code": status_code,
            "message": message,
            "data": data
        }, status=status_code)

    @staticmethod
    def error(message="Something went wrong", data=None, status_code=http_status.HTTP_400_BAD_REQUEST):
        return Response({
            "status_code": status_code,
            "message": message,
            "data": data or []
        }, status=status_code)
