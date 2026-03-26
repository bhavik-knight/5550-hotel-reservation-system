from django.urls import path
from .views import (
    ReservationCreateView,
    ReservationDetailView,
    ReservationListView,
    GuestListCreateView,
    GuestDetailView,
)

urlpatterns = [
    # Assignment Endpoints
    path(
        "reservationConfirmation/", ReservationCreateView.as_view(), name="res-create"
    ),
    path(
        "reservations/<str:confirmation_number>/",
        ReservationDetailView.as_view(),
        name="res-detail",
    ),
    path("reservations/", ReservationListView.as_view(), name="res-list"),
    # Global Guest Management (independent of reservations)
    path("guests/", GuestListCreateView.as_view(), name="guest-list"),
    path("guests/<int:pk>/", GuestDetailView.as_view(), name="guest-detail"),
]
