from django.db import models


class Address(models.Model):
    """Represents a physical address used by hotels and persons.

    Attributes:
        street_address: Street and unit information.
        city: City name.
        province: Province or state.
        postal_code: Postal or ZIP code.
        country: Country name.
    """

    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Canada")

    def __str__(self) -> str:
        """Return a readable address label.

        Returns:
            str: Formatted address string.
        """
        return f"{self.street_address}, {self.city}"
