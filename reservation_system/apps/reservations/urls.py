from django.urls import path
from .views import (
    ReservationCreateView,
    ReservationDetailView,
    PersonListCreateView,
    PersonDetailView,
)

urlpatterns = [
    # Assignment Endpoints
    path(
        "reservationConfirmation/", ReservationCreateView.as_view(), name="res-create"
    ),
    path(
        "reservation/<str:confirmation_number>/",
        ReservationDetailView.as_view(),
        name="res-detail",
    ),
    # Global Person Management (independent of reservations)
    path("people/", PersonListCreateView.as_view(), name="person-list"),
    path("people/<int:pk>/", PersonDetailView.as_view(), name="person-detail"),
]
