from django.urls import path
from .views import HotelListCreateView, HotelListView, HotelRetrieveUpdateDestroyView

urlpatterns = [
    path("getListOfHotels/", HotelListView.as_view(), name="get-list-of-hotels"),
    path("hotels/", HotelListCreateView.as_view(), name="hotel-list-create"),
    path("hotels/<int:id>/", HotelRetrieveUpdateDestroyView.as_view(), name="hotel-detail"),
]
