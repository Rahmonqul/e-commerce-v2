from django.urls import  path
from .views import *

urlpatterns=[
    path('stores/', VendorStoresView.as_view(), name='stores'),
    path('stores/<str:slug>/', VendorDetailView.as_view(), name='steredetail'),
    path('productlist/<str:vendor_store_name>/', ProductToVendor.as_view(), name='steredetailproducts'),
]