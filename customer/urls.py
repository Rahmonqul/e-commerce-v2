from django.urls import path
from .views import AddressListCreateAPIView, AddressRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroyAPIView.as_view(), name='address-retrieve-update-destroy'),
]
