from rest_framework import serializers
from .models import Hotel
from addresses.serializers import AddressSerializer


class HotelSerializer(serializers.ModelSerializer):
    """Serializes Hotel instances with nested address information.

    Attributes:
        address: Nested AddressSerializer for read-only address output.
        Meta.model: The Hotel model to serialize.
        Meta.fields: The list of fields included in the output.
    """

    address = AddressSerializer(read_only=True)

    class Meta:  # type: ignore[override]
        model = Hotel
        fields = ["id", "name", "description", "phone", "email", "base_rate", "address"]
