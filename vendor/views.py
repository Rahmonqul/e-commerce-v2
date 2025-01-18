from django.shortcuts import render
from django.db.models import Count, Avg
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import *
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from store.filters import ProductFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from store.serializers import ProductListSerializer

# Create your views here.
class VendorPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


class VendorStoresView(ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['store_name']
    # filterset_fields = ['store_name']
    pagination_class = VendorPagination

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_queryset(self):
        queryset = Vendor.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(store_name__icontains=search_query)
        return queryset

class VendorDetailView(RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return super().get_queryset()


class ProductToVendor(ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    class Pagination(PageNumberPagination):
        page_size = 12
        page_size_query_param = 'page_size'
        max_page_size = 12

    pagination_class = Pagination

    def get_queryset(self):
        vendor_store_name = self.kwargs['vendor_store_name']
        try:
            vendor = Vendor.objects.get(store_name=vendor_store_name)
            user = vendor.user
        except Vendor.DoesNotExist:
            raise NotFound(detail="Vendor with this store name does not exist.")
        return Product.objects.filter(vendor=user)