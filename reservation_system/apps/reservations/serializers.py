import uuid
from typing import Any

from rest_framework import serializers

from .models import Reservation, Person
from addresses.serializers import AddressSerializer


class PersonSerializer(serializers.ModelSerializer):
    """Serializes Person instances including optional address data.

    Attributes:
        address: Nested AddressSerializer for optional address data.
        Meta.model: The Person model to serialize.
        Meta.fields: The list of fields included in the output.
    """

    address = AddressSerializer(required=False, allow_null=True)

    class Meta:
        model = Person
        fields = ["id", "name", "phone_number", "email", "address"]


class ReservationSerializer(serializers.ModelSerializer):
    """Serializes Reservation instances and nested guest information.

    Attributes:
        guests_list: Nested list of PersonSerializer entries.
        Meta.model: The Reservation model to serialize.
        Meta.fields: The list of fields included in the output.
        Meta.read_only_fields: Fields that are server-generated.
    """

    # Rename 'guests' to 'guests_list' to match assignment spec
    guests_list = PersonSerializer(source="guests", many=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "hotel_name",
            "checkin",
            "checkout",
            "guests_list",
            "confirmation_number",
        ]
        read_only_fields = ["confirmation_number"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the reservation payload.

        Args:
            attrs: Incoming serializer attributes.

        Returns:
            dict[str, Any]: Validated attributes.

        Raises:
            serializers.ValidationError: If the payload is invalid.
        """
        return attrs

    def create(self, validated_data: dict[str, Any]) -> Reservation:
        """Create a reservation and attach guest records.

        Args:
            validated_data: Validated input data for the reservation.

        Returns:
            Reservation: The created reservation instance.

        Raises:
            serializers.ValidationError: If guest data is missing.
        """
        guests_data = validated_data.pop("guests")

        conf_num = f"CONF-{uuid.uuid4().hex[:8].upper()}"

        reservation = Reservation.objects.create(
            confirmation_number=conf_num, **validated_data
        )

        for person_data in guests_data:
            person, created = Person.objects.get_or_create(
                email=person_data.get("email"), defaults=person_data
            )
            reservation.guests.add(person)

        return reservation
