from django.urls import path
from .views import HotelListView

urlpatterns = [
    path('getListOfHotels/', HotelListView.as_view(), name='get-list-of-hotels'),
]
