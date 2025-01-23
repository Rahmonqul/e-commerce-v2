from django.urls import path
from .views import AddressListCreateAPIView, AddressRetrieveUpdateDestroyAPIView, WhishlistView, RemoveProductFromWhishlist
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroyAPIView.as_view(), name='address-retrieve-update-destroy'),
    path('wishlist/',  csrf_exempt(WhishlistView.as_view()), name='wishlist'),
    path('wishlist/remove/<int:product_id>/', RemoveProductFromWhishlist.as_view(), name='remove-product-from-whishlist'),

]
