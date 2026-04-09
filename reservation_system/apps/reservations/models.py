from django.db import models
from apps.hotels.models import Hotel


class Guest(models.Model):
    """Represents a guest who can be associated with reservations.

    Attributes:
        name: Full name of the guest.
        gender: Gender of the guest.
        phone_number: Contact phone number.
        email: Unique email address.
    """

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    reservation = models.ForeignKey(
        "Reservation",
        on_delete=models.CASCADE,
        related_name="guests",
    )

    def __str__(self) -> str:
        """Return a readable guest label.

        Returns:
            str: Formatted name and email.
        """
        return f"{self.name} ({self.email})"


class Reservation(models.Model):
    """Represents a reservation with guests and confirmation metadata.

    Attributes:
        hotel_name: Hotel identifier or name.
        hotel: Related hotel record when available.
        checkin: Check-in date.
        checkout: Check-out date.
        confirmation_number: Unique confirmation token.
        guests: Related guests associated with the reservation.
    """

    hotel_name = models.CharField(max_length=255)
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reservations",
    )
    checkin = models.DateField()
    checkout = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    confirmation_number = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        """Return a readable reservation label.

        Returns:
            str: Formatted hotel name and confirmation number.
        """
        hotel_label = self.hotel.name if self.hotel else self.hotel_name
        return f"{hotel_label} - {self.confirmation_number}"
