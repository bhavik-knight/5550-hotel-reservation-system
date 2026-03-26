from typing import Any

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Reservation, Person
from .serializers import ReservationSerializer, PersonSerializer
from drf_spectacular.utils import extend_schema


# Manage the Global Person Directory (Add/Edit/Delete People)
class PersonListCreateView(generics.ListCreateAPIView):
    """List or create Person records.

    Attributes:
        queryset: The collection of Person instances.
        serializer_class: Serializer for Person data.
    """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single Person record.

    Attributes:
        queryset: The collection of Person instances.
        serializer_class: Serializer for Person data.
    """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer


# Manage Reservations
@extend_schema(
    summary="reservationConfirmation",
    description="Create a reservation and receive a confirmation number",
    operation_id="reservationConfirmation",
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
