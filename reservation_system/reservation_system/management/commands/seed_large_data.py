from __future__ import annotations

from datetime import date, timedelta
from random import choice, randint, sample
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from addresses.models import Address
from hotels.models import Hotel
from reservations.models import Person, Reservation


class Command(BaseCommand):
    """Seed a large, realistic dataset for testing.

    Generates:
        - 70 Address records
        - 20 Hotel records (each linked to one Address)
        - 80 Person records
        - 250 Reservation records

    Use the --clear-db flag to wipe existing data before seeding.
    """

    help = "Seed large dataset for testing (addresses, hotels, persons, reservations)."

    def add_arguments(self, parser) -> None:
        """Register command-line arguments.

        Args:
            parser: Django argument parser instance.

        Returns:
            None
        """
        parser.add_argument(
            "--clear-db",
            action="store_true",
            help="Delete existing records before seeding.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the seed routine.

        Args:
            *args: Positional arguments passed by Django.
            **options: Keyword options passed by Django.

        Returns:
            None
        """
        clear_db = bool(options.get("clear_db"))

        if not clear_db and (
            Address.objects.exists()
            or Hotel.objects.exists()
            or Person.objects.exists()
            or Reservation.objects.exists()
        ):
            self.stdout.write(
                self.style.WARNING(
                    "Existing data detected. Use --clear-db to reseed safely."
                )
            )
            return

        faker = Faker("en_CA")
        provinces = ["NS", "ON", "BC", "AB", "MB", "SK", "QC", "NB", "NL", "PE"]

        with transaction.atomic():
            if clear_db:
                Reservation.objects.all().delete()
                Person.objects.all().delete()
                Hotel.objects.all().delete()
                Address.objects.all().delete()

            addresses: list[Address] = []
            for _ in range(70):
                address = Address.objects.create(
                    street_address=faker.street_address(),
                    city=faker.city(),
                    province=choice(provinces),
                    postal_code=faker.postcode(),
                    country="Canada",
                )
                addresses.append(address)

            hotels: list[Hotel] = []
            hotel_address_pool = sample(addresses, k=20)
            for index, address in enumerate(hotel_address_pool, start=1):
                hotel = Hotel.objects.create(
                    name=f"{faker.company()} Hotel {index}",
                    description=faker.sentence(nb_words=10),
                    phone=faker.phone_number(),
                    email=f"reservations{index}@{faker.domain_name()}",
                    base_rate=f"{randint(120, 320)}.00",
                    address=address,
                )
                hotels.append(hotel)

            persons: list[Person] = []
            for _ in range(80):
                full_name = faker.name()
                person = Person.objects.create(
                    name=full_name,
                    phone_number=faker.phone_number(),
                    email=faker.unique.email(),
                    address=choice(addresses),
                )
                persons.append(person)

            for _ in range(250):
                checkin = date(2026, 1, 1) + timedelta(days=randint(0, 364))
                checkout = checkin + timedelta(days=randint(1, 10))
                reservation = Reservation.objects.create(
                    hotel_name=choice(hotels).name,
                    checkin=checkin,
                    checkout=checkout,
                    confirmation_number=f"CONF-{faker.unique.bothify(text='????-####').upper()}",
                )
                guest_count = randint(1, 3)
                reservation.guests.add(*sample(persons, k=guest_count))

        self.stdout.write(
            self.style.SUCCESS(
                "Seed complete: 70 addresses, 20 hotels, 80 persons, 250 reservations."
            )
        )
