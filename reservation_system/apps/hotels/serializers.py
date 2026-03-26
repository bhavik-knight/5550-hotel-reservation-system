from rest_framework import serializers
from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    """Serializes Hotel instances.

    Attributes:
        Meta.model: The Hotel model to serialize.
        Meta.fields: The list of fields included in the output.
    """

    class Meta:  # type: ignore[override]
        model = Hotel
        fields = ["id", "name", "description", "phone", "email", "base_rate"]
