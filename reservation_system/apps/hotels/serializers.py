from rest_framework import serializers
from .models import Hotel
from addresses.serializers import AddressSerializer


class HotelSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'phone', 'email', 'base_rate', 'address']
