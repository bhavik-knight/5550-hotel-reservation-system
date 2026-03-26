import uuid
from typing import Any

from django.utils import timezone
from rest_framework import serializers

from hotels.models import Hotel
from .models import Guest, Reservation


class GuestSerializer(serializers.ModelSerializer):
    """Serializes Guest instances.

    Attributes:
        Meta.model: The Guest model to serialize.
        Meta.fields: The list of fields included in the output.
    """

    class Meta:  # type: ignore[override]
        model = Guest
        fields = [
            "id",
            "name",
            "gender",
            "phone_number",
            "email",
        ]

    def validate_name(self, value: str) -> str:
        """Validate guest name input.

        Args:
            value: Guest name value.

        Returns:
            str: Normalized name string.
        """
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("name must be at least 2 characters.")
        return value

    def validate_phone_number(self, value: str) -> str:
        """Validate phone number input.

        Args:
            value: Phone number value.

        Returns:
            str: Normalized phone number string.
        """
        cleaned = "".join(ch for ch in value if ch.isdigit())
        if len(cleaned) < 7:
            raise serializers.ValidationError("phone_number is invalid.")
        return value


class HotelCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating or linking Hotel records."""

    class Meta:  # type: ignore[override]
        model = Hotel
        fields = [
            "name",
            "description",
            "phone",
            "email",
            "base_rate",
        ]

    def create(self, validated_data: dict[str, Any]) -> Hotel:
        """Create or update a Hotel record.

        Args:
            validated_data: Validated hotel payload.

        Returns:
            Hotel: The created hotel instance.
        """
        hotel, created = Hotel.objects.get_or_create(
            name=validated_data["name"],
            defaults=validated_data,
        )
        if not created:
            for key, value in validated_data.items():
                setattr(hotel, key, value)
            hotel.save()

        return hotel


class ReservationSerializer(serializers.ModelSerializer):
    """Serializes Reservation instances and nested guest information.

    Attributes:
        guests_list: Nested list of GuestSerializer entries.
        Meta.model: The Reservation model to serialize.
        Meta.fields: The list of fields included in the output.
        Meta.read_only_fields: Fields that are server-generated.
    """

    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    class GuestInputSerializer(serializers.Serializer):
        """Input serializer for guest list.

        Attributes:
            guest_name: Name of the guest.
            gender: Gender of the guest.
        """

        guest_name = serializers.CharField(max_length=255)
        gender = serializers.CharField(max_length=20)

        def validate_guest_name(self, value: str) -> str:
            """Validate guest name input.

            Args:
                value: Guest name value.

            Returns:
                str: Normalized guest name.
            """
            value = value.strip()
            if not value:
                raise serializers.ValidationError("guest_name cannot be empty.")
            return value

        def validate_gender(self, value: str) -> str:
            """Validate gender input.

            Args:
                value: Gender value.

            Returns:
                str: Normalized gender string.
            """
            value = value.strip()
            if not value:
                raise serializers.ValidationError("gender cannot be empty.")
            allowed = {"male", "female", "other", "prefer not to say"}
            if value.lower() not in allowed:
                raise serializers.ValidationError(
                    "gender must be Male, Female, Other, or Prefer not to say."
                )
            return value

    guests_list = GuestInputSerializer(many=True, write_only=True, required=False)
    guests_details = GuestSerializer(source="guests", many=True, read_only=True)

    class Meta:  # type: ignore[override]
        model = Reservation
        fields = [
            "id",
            "hotel_name",
            "checkin",
            "checkout",
            "price",
            "guests_list",
            "guests_details",
            "confirmation_number",
        ]
        read_only_fields = ["confirmation_number"]

    def get_fields(self) -> dict[str, serializers.Field]:
        """Customize fields for the browsable API form.

        Returns:
            dict[str, serializers.Field]: Serializer fields.
        """
        fields = super().get_fields()
        request = self.context.get("request")
        if request and getattr(request, "accepted_renderer", None):
            if request.accepted_renderer.format == "html":
                pass

        return fields

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the reservation payload.

        Args:
            attrs: Incoming serializer attributes.

        Returns:
            dict[str, Any]: Validated attributes.

        Raises:
            serializers.ValidationError: If the payload is invalid.
        """
        if not self.initial_data.get("hotel_name"):
            raise serializers.ValidationError("Provide hotel_name.")

        if not self.initial_data.get("guests_list"):
            raise serializers.ValidationError("Provide guests_list.")

        if attrs.get("price") is None:
            raise serializers.ValidationError("Provide price.")

        price = attrs.get("price")
        if price is not None and price < 0:
            raise serializers.ValidationError("price cannot be negative.")

        checkin = attrs.get("checkin")
        checkout = attrs.get("checkout")
        today = timezone.now().date()
        if checkin and checkin < today:
            raise serializers.ValidationError("checkin cannot be in the past.")
        if checkin and checkin > today.replace(year=today.year + 1):
            raise serializers.ValidationError(
                "checkin cannot be more than 1 year in the future."
            )
        if checkin and checkout and checkout <= checkin:
            raise serializers.ValidationError("checkout must be after checkin.")

        return attrs

    def validate_hotel_name(self, value: str) -> str:
        """Validate hotel name input.

        Args:
            value: Hotel name value.

        Returns:
            str: Normalized hotel name string.
        """
        value = value.strip()
        if not value:
            raise serializers.ValidationError("hotel_name cannot be empty.")
        return value

    def create(self, validated_data: dict[str, Any]) -> Reservation:
        """Create a reservation and attach guest records.

        Args:
            validated_data: Validated input data for the reservation.

        Returns:
            Reservation: The created reservation instance.

        Raises:
            serializers.ValidationError: If guest data is missing.
        """
        guests_list = validated_data.pop("guests_list", [])
        hotel_name = validated_data.get("hotel_name")

        if not hotel_name:
            raise serializers.ValidationError("Hotel name is required.")

        conf_num = f"CONF-{uuid.uuid4().hex[:8].upper()}"

        reservation = Reservation.objects.create(
            confirmation_number=conf_num, **validated_data
        )

        for guest in guests_list:
            guest_name = guest.get("guest_name")
            gender = guest.get("gender", "")
            email = f"guest-{uuid.uuid4().hex[:12]}@example.com"
            guest_record = Guest.objects.create(
                name=guest_name,
                gender=gender,
                phone_number="000-000-0000",
                email=email,
            )
            reservation.guests.add(guest_record)

        return reservation
