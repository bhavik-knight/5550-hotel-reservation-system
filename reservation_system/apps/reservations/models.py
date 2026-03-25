from django.db import models
from addresses.models import Address

class Person(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    # Adding address to Person
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='persons')

    def __str__(self):
        return f"{self.name} ({self.email})"


class Reservation(models.Model):
    hotel_name = models.CharField(max_length=255)
    checkin = models.DateField()
    checkout = models.DateField()
    confirmation_number = models.CharField(max_length=100, unique=True)

    # Many-to-Many allows a Person to have many reservations
    # and a Reservation to have many guests (People).
    guests = models.ManyToManyField(Person, related_name='reservations')

    def __str__(self):
        return f"{self.hotel_name} - {self.confirmation_number}"