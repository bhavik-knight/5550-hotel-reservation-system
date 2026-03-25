from rest_framework import generics
from .models import Reservation, Person
from .serializers import ReservationSerializer, PersonSerializer
from drf_spectacular.utils import extend_schema

# Manage the Global Person Directory (Add/Edit/Delete People)
class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

# Manage Reservations
@extend_schema(
    summary="reservationConfirmation",
    description="Create a reservation and receive a confirmation number",
    operation_id="reservationConfirmation",
)
class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'confirmation_number'