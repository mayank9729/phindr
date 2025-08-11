from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import SupportTicket
from .serializer import SupportTicketSerializer
from core.utils.response_handler import ResponseHandler 


class SupportTicketViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Create Ticket
    def create_ticket(self, request):
        serializer = SupportTicketSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            ticket = serializer.save()
            return ResponseHandler.success(
                message="Ticket created successfully",
                data={
                    "ticket_id": str(ticket.ticket_id),
                    "status": ticket.status
                },
                status_code=status.HTTP_201_CREATED
            )
        return ResponseHandler.error(
            message="Validation failed",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Change Status
    def change_status(self, request, pk=None):
        ticket = get_object_or_404(SupportTicket, pk=pk)
        new_status = request.data.get("status")

        if new_status not in ['open', 'closed']:
            return ResponseHandler.error("Invalid status. Must be 'open' or 'closed'.")

        if ticket.status == new_status:
            return ResponseHandler.error(f"Ticket is already {new_status}.")
        
        if new_status == "closed":
            if not (request.user.is_staff or request.user.is_superuser):
                return ResponseHandler.error(
                    "Only admin or staff can close a ticket.",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            ticket.closed_by = request.user
        else:
            ticket.closed_by = None 

        ticket.status = new_status
        ticket.save()

        return ResponseHandler.success(
            message=f"Ticket status changed to {new_status}",
            data={
                    "ticket_id": str(ticket.ticket_id),
                    "status": ticket.status
                },
                status_code=status.HTTP_201_CREATED)

    # List Tickets with filter & sort
    def list_tickets(self, request):
        status_filter = request.query_params.get("status")
        sort_order = request.query_params.get("sort", "date")

        tickets = SupportTicket.objects.all()

        if status_filter in ['open', 'closed']:
            tickets = tickets.filter(status=status_filter)

        tickets = tickets.order_by("-date" if sort_order == "desc" else "date")

        data = [
            {
                "id": ticket.id,
                "ticket_id": str(ticket.ticket_id),
                "date": ticket.date,
                "reason": ticket.reason,
                "query_type": ticket.query_type,
                "status": ticket.status,
                "raised_by": str(ticket.raised_by),
                "closed_by": str(ticket.closed_by) if ticket.closed_by else None
            }
            for ticket in tickets
        ]
        return ResponseHandler.success(data=data)
