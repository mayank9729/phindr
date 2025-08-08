from rest_framework import serializers
from .models import SupportTicket

class SupportTicketSerializer(serializers.Serializer):
    reason=serializers.CharField(max_length=500)
    query_type=serializers.CharField(max_length=20)
    
    def validate_reason(self,value):
        if not value.strip():
            raise serializers.ValidationError("Reason cannot be empty!!")
        if len(value)<10:
            raise serializers.ValidationError("Reason must be atleast of 10 characters.")
        return value
    
    def validate_query (self,value):
        valid_type = dict(SupportTicket.QUERY_TYPES).keys()
        if not value in valid_type:
            raise serializer.ValidationError(f"Invalid query type!, must  be one of {', '.join(valid_type)} ")
        return value
        
    def create(self, validated_data):
        user = self.context['request'].user
        return SupportTicket.objects.create(
            reason=validated_data['reason'],
            query_type=validated_data['query_type'],
            raised_by=user
        )
        