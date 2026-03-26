from typing import Any

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Guest, Reservation
from .serializers import GuestSerializer, ReservationSerializer
from drf_spectacular.utils import OpenApiExample, extend_schema


# Manage the Global Guest Directory (Add/Edit/Delete Guests)
class GuestListCreateView(generics.ListCreateAPIView):
    """List or create Guest records.

    Attributes:
        queryset: The collection of Guest instances.
        serializer_class: Serializer for Guest data.
    """

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single Guest record.

    Attributes:
        queryset: The collection of Guest instances.
        serializer_class: Serializer for Guest data.
    """

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# Manage Reservations
@extend_schema(
    summary="reservationConfirmation",
    description="Create a reservation and receive a confirmation number",
    operation_id="reservationConfirmation",
    examples=[
        OpenApiExample(
            "ReservationRequest",
            value={
                "hotel_name": "Grand Hotel Downtown",
                "checkin": "2026-04-15",
                "checkout": "2026-04-18",
                "price": "299.99",
                "guests_list": [
                    {"guest_name": "John Doe", "gender": "Male"},
                    {"guest_name": "Jane Smith", "gender": "Female"},
                ],
            },
            request_only=True,
        ),
        OpenApiExample(
            "ReservationResponse",
            value={
                "id": 1,
                "hotel_name": "Grand Hotel Downtown",
                "checkin": "2026-04-15",
                "checkout": "2026-04-18",
                "price": "299.99",
                "confirmation_number": "CONF-A1B2C3D4",
                "guests_details": [
                    {
                        "id": 10,
                        "name": "John Doe",
                        "gender": "Male",
                        "phone_number": "000-000-0000",
                        "email": "guest-abc123@example.com",
                    },
                    {
                        "id": 11,
                        "name": "Jane Smith",
                        "gender": "Female",
                        "phone_number": "000-000-0000",
                        "email": "guest-def456@example.com",
                    },
                ],
            },
            response_only=True,
        ),
    ],
)
class ReservationCreateView(generics.CreateAPIView):
    """Function Name: reservationConfirmation

    HTTP Method: POST

    Description:
        Creates a reservation and returns a confirmation number.

    Attributes:
        queryset: The collection of Reservation instances.
        serializer_class: Serializer for Reservation data.
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Handle POST requests to create a reservation.

        Args:
            request: The incoming REST framework request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The created reservation payload with confirmation number.
        """
        return super().post(request, *args, **kwargs)


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a reservation by confirmation number.

    Attributes:
        queryset: The collection of Reservation instances.
        serializer_class: Serializer for Reservation data.
        lookup_field: The field used to locate a reservation.
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = "confirmation_number"


@extend_schema(
    summary="getAllReservations",
    description="Return a list of all reservations",
    operation_id="getAllReservations",
)
class ReservationListView(generics.ListAPIView):
    """Function Name: getAllReservations

    HTTP Method: GET

    Description:
        Returns all reservations in the system.

    Attributes:
        queryset: The collection of Reservation instances.
        serializer_class: Serializer for Reservation data.
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
