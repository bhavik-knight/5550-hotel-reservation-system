from typing import Any

from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Hotel
from apps.reservations.models import Reservation
from .serializers import HotelSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(
    summary="getListOfHotels",
    description="This endpoint returns the list of hotels",
    operation_id="getListOfHotels",
)
class HotelListView(generics.ListAPIView):
    """Function Name: getListOfHotels

    HTTP Method: GET

    Description:
        This endpoint returns the list of hotels.

    Attributes:
        queryset: The collection of Hotel instances to be serialized.
        serializer_class: The serializer used to convert models to JSON.
    """

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_queryset(self):
        """Filter hotels by optional check-in/check-out query params.

        Returns:
            QuerySet: Filtered set of hotels.
        """
        queryset = super().get_queryset()
        checkin_raw = self.request.query_params.get("checkin")
        checkout_raw = self.request.query_params.get("checkout")
        checkin = parse_date(checkin_raw) if checkin_raw else None
        checkout = parse_date(checkout_raw) if checkout_raw else None

        if not checkin or not checkout:
            return queryset

        overlapping = Reservation.objects.filter(
            hotel__isnull=False,
            checkin__lt=checkout,
            checkout__gt=checkin,
        ).values_list("hotel_id", flat=True)

        return queryset.exclude(id__in=overlapping)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Handle GET requests for a list of hotels.

        Args:
            request: The incoming REST framework request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A list of serialized hotel data.
        """
        return super().get(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        summary="listHotels",
        description="List all hotels.",
        operation_id="listHotels",
    ),
    post=extend_schema(
        summary="createHotel",
        description="Create a new hotel.",
        operation_id="createHotel",
    ),
)
class HotelListCreateView(generics.ListCreateAPIView):
    """List or create hotels.

    HTTP Methods: GET, POST
    """

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


@extend_schema_view(
    get=extend_schema(
        summary="getHotel",
        description="Retrieve a hotel by ID.",
        operation_id="getHotel",
    ),
    put=extend_schema(
        summary="updateHotel",
        description="Update a hotel by ID.",
        operation_id="updateHotel",
    ),
    patch=extend_schema(
        summary="partialUpdateHotel",
        description="Partially update a hotel by ID.",
        operation_id="partialUpdateHotel",
    ),
    delete=extend_schema(
        summary="deleteHotel",
        description="Delete a hotel by ID.",
        operation_id="deleteHotel",
    ),
)
class HotelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a hotel.

    HTTP Methods: GET, PUT, PATCH, DELETE
    """

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    lookup_field = "id"


@extend_schema(
    summary="getHotelById",
    description="Retrieve hotel details by ID",
    operation_id="getHotelById",
)
class HotelDetailView(generics.RetrieveAPIView):
    """Function Name: getHotelById

    HTTP Method: GET

    Description:
        Retrieve a single hotel record by its ID.

    Attributes:
        queryset: The collection of Hotel instances to be serialized.
        serializer_class: The serializer used to convert models to JSON.
        lookup_field: Field used for lookup.
    """

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    lookup_field = "id"
