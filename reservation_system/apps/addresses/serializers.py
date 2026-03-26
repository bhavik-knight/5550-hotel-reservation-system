from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    """Serializes Address instances for API responses.

    Attributes:
        Meta.model: The Address model to serialize.
        Meta.fields: The list of fields included in the output.
    """

    class Meta:
        model = Address
        fields = ["id", "street_address", "city", "province", "postal_code", "country"]
