from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from addresses.models import Address
from hotels.models import Hotel


class Command(BaseCommand):
    """Seed the database with sample hotel and address data.

    This command is idempotent: it uses get_or_create to avoid duplicates
    if it is run multiple times.
    """

    help = "Seed the database with sample hotels and addresses."

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the seed routine.

        Args:
            *args: Positional arguments passed by Django.
            **options: Keyword options passed by Django.

        Returns:
            None
        """
        hotels_payload: list[dict[str, Any]] = [
            {
                "name": "Harborfront Suites",
                "description": "Waterfront boutique hotel near the boardwalk.",
                "phone": "+1-902-555-0101",
                "email": "info@harborfrontsuites.ca",
                "base_rate": "189.00",
                "address": {
                    "street_address": "12 Oceanview Dr",
                    "city": "Halifax",
                    "province": "NS",
                    "postal_code": "B3H 1Y6",
                    "country": "Canada",
                },
            },
            {
                "name": "Maple Leaf Grand",
                "description": "Downtown hotel with skyline views.",
                "phone": "+1-416-555-0198",
                "email": "stay@mapleleafgrand.ca",
                "base_rate": "229.00",
                "address": {
                    "street_address": "250 King St W",
                    "city": "Toronto",
                    "province": "ON",
                    "postal_code": "M5V 1H9",
                    "country": "Canada",
                },
            },
            {
                "name": "Pacific Crest Hotel",
                "description": "Modern suites close to the seawall.",
                "phone": "+1-604-555-0134",
                "email": "hello@pacificcrest.ca",
                "base_rate": "245.00",
                "address": {
                    "street_address": "88 Seawall Ave",
                    "city": "Vancouver",
                    "province": "BC",
                    "postal_code": "V6B 5K3",
                    "country": "Canada",
                },
            },
            {
                "name": "Prairie Sky Inn",
                "description": "Business-friendly stay near the river valley.",
                "phone": "+1-780-555-0172",
                "email": "reservations@prairiesky.ca",
                "base_rate": "165.00",
                "address": {
                    "street_address": "510 Jasper Ave",
                    "city": "Edmonton",
                    "province": "AB",
                    "postal_code": "T5J 1N3",
                    "country": "Canada",
                },
            },
            {
                "name": "Capital Heritage Hotel",
                "description": "Historic property steps from Parliament Hill.",
                "phone": "+1-613-555-0117",
                "email": "frontdesk@capitalheritage.ca",
                "base_rate": "210.00",
                "address": {
                    "street_address": "45 Wellington St",
                    "city": "Ottawa",
                    "province": "ON",
                    "postal_code": "K1A 0A9",
                    "country": "Canada",
                },
            },
        ]

        created_hotels = 0
        created_addresses = 0

        with transaction.atomic():
            for payload in hotels_payload:
                address_data = payload.pop("address")
                address, address_created = Address.objects.get_or_create(
                    street_address=address_data["street_address"],
                    city=address_data["city"],
                    province=address_data["province"],
                    postal_code=address_data["postal_code"],
                    defaults={"country": address_data.get("country", "Canada")},
                )

                if address_created:
                    created_addresses += 1

                hotel, hotel_created = Hotel.objects.get_or_create(
                    name=payload["name"],
                    defaults={
                        "description": payload["description"],
                        "phone": payload["phone"],
                        "email": payload["email"],
                        "base_rate": payload["base_rate"],
                        "address": address,
                    },
                )

                if not hotel_created:
                    hotel.address = address
                    hotel.description = payload["description"]
                    hotel.phone = payload["phone"]
                    hotel.email = payload["email"]
                    hotel.base_rate = payload["base_rate"]
                    hotel.save()
                else:
                    created_hotels += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Hotels created: {created_hotels}. "
                f"Addresses created: {created_addresses}."
            )
        )
