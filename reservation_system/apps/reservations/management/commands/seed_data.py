import random
import uuid
from django.core.management.base import BaseCommand
from faker import Faker
from model_bakery import baker
from apps.hotels.models import Hotel
from apps.reservations.models import Reservation, Guest

fake = Faker()

class Command(BaseCommand):
    help = "Seeds the database with specific counts of realistic mock data."

    def add_arguments(self, parser):
        parser.add_argument('--hotels', type=int, default=20)
        parser.add_argument('--reservations', type=int, default=250)

    def handle(self, *args, **options):
        num_hotels = options['hotels']
        num_reservations = options['reservations']

        # Clear existing data in correct order to respect PROTECT/CASCADE
        Guest.objects.all().delete()
        Reservation.objects.all().delete()
        Hotel.objects.all().delete()

        self.stdout.write(f"Seeding {num_hotels} hotels...")
        
        prefixes = ["Grand", "Royal", "Sunset", "Alpine", "Urban", "Crystal", "Golden", "Emerald", "Harbor", "Emerald"]
        suffixes = ["Plaza", "Resort", "Hotel", "Suites", "Lodge", "Inn", "Manor", "Garden", "Gateway", "Palace"]
        locations = ["Downtown", "Beachside", "Central", "East", "West", "Park", "Highlands", "Valley"]

        hotels = []
        for i in range(num_hotels):
            name = f"{random.choice(prefixes)} {random.choice(locations)} {random.choice(suffixes)}"
            # Ensure uniqueness if random choices collide
            if Hotel.objects.filter(name=name).exists():
                name = f"{name} {i}"
                
            hotel = baker.make(
                Hotel,
                name=name,
                description=fake.paragraph(nb_sentences=3),
                phone=fake.phone_number()[:20],
                email=fake.unique.company_email(),
                base_rate=random.randint(99, 899)
            )
            hotels.append(hotel)

        self.stdout.write(f"Seeding {num_reservations} reservations...")
        for _ in range(num_reservations):
            hotel = random.choice(hotels)
            conf_num = f"CONF-{uuid.uuid4().hex[:10].upper()}"
            
            reservation = baker.make(
                Reservation,
                hotel=hotel,
                hotel_name=hotel.name,
                confirmation_number=conf_num,
                checkin=fake.date_between(start_date='today', end_date='+60d'),
                checkout=fake.date_between(start_date='+61d', end_date='+90d'),
                price=random.randint(150, 3000)
            )
            
            # Since the current schema requires 1 Guest per 1 Reservation (FK),
            # and the user wants 250 reservations, we must have at least 250 guest records.
            # We will create exactly 1 guest for most, and 2-3 for some, 
            # to keep the data interesting.
            num_guests = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
            for _ in range(num_guests):
                baker.make(
                    Guest,
                    name=fake.name(),
                    gender=random.choice(["Male", "Female", "Other", "Prefer not to say"]),
                    phone_number=fake.phone_number()[:20],
                    email=fake.unique.email(),
                    reservation=reservation
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded: {Hotel.objects.count()} Hotels, {Reservation.objects.count()} Reservations, {Guest.objects.count()} Guests!"))
