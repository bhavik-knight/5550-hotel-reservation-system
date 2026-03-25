from rest_framework import generics
from .models import Hotel
from .serializers import HotelSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="getListOfHotels",
    description="This endpoint returns the list of hotels",
    operation_id="getListOfHotels",
)
class HotelListView(generics.ListAPIView):
    """Returns a list of all hotels.

    Matches the reservations app pattern: simple generics-based CBV.
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
