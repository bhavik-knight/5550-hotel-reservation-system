from rest_framework import serializers
from .models import Reservation, Person
from addresses.serializers import AddressSerializer


class PersonSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False, allow_null=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'phone_number', 'email', 'address']


class ReservationSerializer(serializers.ModelSerializer):
    # Rename 'guests' to 'guests_list' to match assignment spec
    guests_list = PersonSerializer(source='guests', many=True)

    class Meta:
        model = Reservation
        fields = ['id', 'hotel_name', 'checkin', 'checkout', 'guests_list', 'confirmation_number']
        read_only_fields = ['confirmation_number']

    def create(self, validated_data):
        guests_data = validated_data.pop('guests')  # Extract nested people data
        import uuid
        conf_num = f"CONF-{uuid.uuid4().hex[:8].upper()}"

        reservation = Reservation.objects.create(confirmation_number=conf_num, **validated_data)

        for person_data in guests_data:
            # Look up by email (unique) or create if they don't exist
            person, created = Person.objects.get_or_create(
                email=person_data.get('email'),
                defaults=person_data
            )
            reservation.guests.add(person)

        return reservation