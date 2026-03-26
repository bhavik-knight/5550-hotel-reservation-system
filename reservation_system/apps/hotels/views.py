from typing import Any

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Hotel
from .serializers import HotelSerializer
from drf_spectacular.utils import extend_schema


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
