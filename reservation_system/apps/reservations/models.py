from django.db import models
from addresses.models import Address


class Person(models.Model):
    """Represents a guest who can be associated with reservations.

    Attributes:
        name: Full name of the person.
        phone_number: Contact phone number.
        email: Unique email address.
        address: Optional reference to an Address record.
    """

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    # Adding address to Person
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="persons",
    )

    def __str__(self) -> str:
        """Return a readable person label.

        Returns:
            str: Formatted name and email.
        """
        return f"{self.name} ({self.email})"


class Reservation(models.Model):
    """Represents a reservation with guests and confirmation metadata.

    Attributes:
        hotel_name: Hotel identifier or name.
        checkin: Check-in date.
        checkout: Check-out date.
        confirmation_number: Unique confirmation token.
        guests: Related guests associated with the reservation.
    """

    hotel_name = models.CharField(max_length=255)
    checkin = models.DateField()
    checkout = models.DateField()
    confirmation_number = models.CharField(max_length=100, unique=True)

    # Many-to-Many allows a Person to have many reservations
    # and a Reservation to have many guests (People).
    guests = models.ManyToManyField(Person, related_name="reservations")

    def __str__(self) -> str:
        """Return a readable reservation label.

        Returns:
            str: Formatted hotel name and confirmation number.
        """
        return f"{self.hotel_name} - {self.confirmation_number}"
