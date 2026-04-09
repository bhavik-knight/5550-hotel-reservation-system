from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from apps.hotels.models import Hotel
from .models import Guest, Reservation


class ReservationGuestTests(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()

	def test_reservation_creates_guest_records(self) -> None:
		# Ensure a hotel exists for the reservation
		Hotel.objects.create(
			name="Test Hotel",
			description="A test hotel",
			phone="123456789",
			email="test@example.com",
			base_rate="100.00"
		)
		checkin = timezone.now().date() + timedelta(days=2)
		checkout = checkin + timedelta(days=3)
		payload = {
			"hotel_name": "Test Hotel",
			"checkin": checkin.isoformat(),
			"checkout": checkout.isoformat(),
			"price": "199.99",
			"guests_list": [
				{"guest_name": "Alice Guest", "gender": "Female"},
				{"guest_name": "Bob Guest", "gender": "Male"},
			],
		}

		response = self.client.post(
			reverse("res-create"),
			data=payload,
			format="json",
		)

		self.assertEqual(response.status_code, 201)
		reservation = Reservation.objects.get(id=response.data["id"])
		guests = Guest.objects.filter(reservation=reservation)

		self.assertEqual(guests.count(), 2)
		self.assertSetEqual(
			set(guests.values_list("name", flat=True)),
			{"Alice Guest", "Bob Guest"},
		)

	def test_reservation_requires_existing_hotel(self) -> None:
		checkin = timezone.now().date() + timedelta(days=2)
		checkout = checkin + timedelta(days=3)
		payload = {
			"hotel_name": "Missing Hotel",
			"checkin": checkin.isoformat(),
			"checkout": checkout.isoformat(),
			"price": "199.99",
			"guests_list": [
				{"guest_name": "Alice Guest", "gender": "Female"},
			],
		}

		response = self.client.post(
			reverse("res-create"),
			data=payload,
			format="json",
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn("hotel_name", response.data)
