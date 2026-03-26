from __future__ import annotations

from datetime import date, timedelta
from random import choice, randint, sample
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from hotels.models import Hotel  # type: ignore[import-not-found]
from reservations.models import Guest, Reservation  # type: ignore[import-not-found]


class Command(BaseCommand):
    """Seed a large, realistic dataset for testing.

    Generates:
        - 20 Hotel records
        - 80 Guest records
        - 250 Reservation records

    Use the --clear-db flag to wipe existing data before seeding.
    """

    help = "Seed large dataset for testing (hotels, guests, reservations)."

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
            Hotel.objects.exists()
            or Guest.objects.exists()
            or Reservation.objects.exists()
        ):
            self.stdout.write(
                self.style.WARNING(
                    "Existing data detected. Use --clear-db to reseed safely."
                )
            )
            return

        faker = Faker("en_CA")

        with transaction.atomic():
            if clear_db:
                Reservation.objects.all().delete()
                Guest.objects.all().delete()
                Hotel.objects.all().delete()

            hotels: list[Hotel] = []
            for index in range(1, 21):
                hotel = Hotel.objects.create(
                    name=f"{faker.company()} Hotel {index}",
                    description=faker.sentence(nb_words=10),
                    phone=faker.phone_number(),
                    email=f"reservations{index}@{faker.domain_name()}",
                    base_rate=f"{randint(120, 320)}.00",
                )
                hotels.append(hotel)

            guests: list[Guest] = []
            for _ in range(80):
                full_name = faker.name()
                guest = Guest.objects.create(
                    name=full_name,
                    phone_number=faker.phone_number(),
                    email=faker.unique.email(),
                )
                guests.append(guest)

            for _ in range(250):
                checkin = date(2026, 1, 1) + timedelta(days=randint(0, 364))
                checkout = checkin + timedelta(days=randint(1, 10))
                hotel = choice(hotels)
                reservation = Reservation.objects.create(
                    hotel_name=hotel.name,
                    hotel=hotel,
                    checkin=checkin,
                    checkout=checkout,
                    price=hotel.base_rate,
                    confirmation_number=f"CONF-{faker.unique.bothify(text='????-####').upper()}",
                )
                guest_count = randint(1, 3)
                reservation.guests.add(*sample(guests, k=guest_count))

        self.stdout.write(
            self.style.SUCCESS(
                "Seed complete: 20 hotels, 80 guests, 250 reservations."
            )
        )
