from django.db import models
from addresses.models import Address


class Hotel(models.Model):
    """Represents a hotel entity with contact and pricing details.

    Attributes:
        name: Hotel name.
        description: Optional description text.
        phone: Contact phone number.
        email: Contact email address.
        base_rate: Base nightly rate.
        address: One-to-one relationship to Address.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, related_name="hotel"
    )

    def __str__(self) -> str:
        """Return a readable hotel label.

        Returns:
            str: Hotel name.
        """
        return self.name
