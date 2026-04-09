import pytest
from django.urls import reverse
from model_bakery import baker
from apps.hotels.models import Hotel
from apps.reservations.models import Reservation, Guest
from datetime import timedelta
from django.utils import timezone

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.mark.django_db
class TestHotelEndpoints:
    def test_list_hotels(self, api_client):
        baker.make(Hotel, _quantity=3)
        url = reverse('hotel-list-create')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_hotel(self, api_client):
        url = reverse('hotel-list-create')
        payload = {
            "name": "Luxury Plaza",
            "description": "A fancy hotel",
            "phone": "1234567890",
            "email": "luxury@example.com",
            "base_rate": "250.00"
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == 201
        assert Hotel.objects.filter(name="Luxury Plaza").exists()

    def test_get_hotel_detail(self, api_client):
        hotel = baker.make(Hotel)
        url = reverse('hotel-detail', kwargs={'id': hotel.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['name'] == hotel.name

    def test_update_hotel(self, api_client):
        hotel = baker.make(Hotel, name="Old Name")
        url = reverse('hotel-detail', kwargs={'id': hotel.id})
        response = api_client.patch(url, {"name": "New Name"}, format='json')
        assert response.status_code == 200
        hotel.refresh_from_db()
        assert hotel.name == "New Name"

    def test_delete_hotel(self, api_client):
        hotel = baker.make(Hotel)
        url = reverse('hotel-detail', kwargs={'id': hotel.id})
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Hotel.objects.filter(id=hotel.id).exists()

    def test_get_list_of_hotels_availability(self, api_client):
        hotel = baker.make(Hotel)
        url = reverse('get-list-of-hotels')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1

@pytest.mark.django_db
class TestReservationEndpoints:
    def test_create_reservation(self, api_client):
        hotel = baker.make(Hotel, name="Target Hotel")
        url = reverse('res-create')
        checkin = timezone.now().date() + timedelta(days=5)
        checkout = checkin + timedelta(days=2)
        payload = {
            "hotel_name": "Target Hotel",
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
            "price": "500.00",
            "guests_list": [
                {"guest_name": "Mark Miller", "gender": "Male"},
                {"guest_name": "Sarah Smith", "gender": "Female"}
            ]
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == 201
        assert Reservation.objects.count() == 1
        assert Guest.objects.count() == 2

    def test_list_reservations(self, api_client):
        baker.make(Reservation, _quantity=2)
        url = reverse('res-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_get_reservation_by_confirmation(self, api_client):
        res = baker.make(Reservation, confirmation_number="CNF123")
        url = reverse('res-detail', kwargs={'confirmation_number': "CNF123"})
        response = api_client.get(url)
        assert response.status_code == 200
        # Using the key with a space as per Serializer's to_representation logic
        assert response.data['confirmation number'] == "CNF123"

@pytest.mark.django_db
class TestGuestEndpoints:
    def test_list_guests(self, api_client):
        baker.make(Guest, _quantity=5)
        url = reverse('guest-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 5

    def test_guest_detail(self, api_client):
        guest = baker.make(Guest)
        url = reverse('guest-detail', kwargs={'pk': guest.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['name'] == guest.name
