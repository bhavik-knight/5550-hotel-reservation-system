from rest_framework import generics
from .models import Hotel
from .serializers import HotelSerializer


class HotelListView(generics.ListAPIView):
    """Returns a list of all hotels.

    Matches the reservations app pattern: simple generics-based CBV.
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
from django.shortcuts import render

# Create your views here.
