from django.urls import  path
from .views import *
from django.urls import include
from . import views


urlpatterns=[
    path('products/', ProductApiView.as_view(), name='productapi'),
    path('reviews/', ReviewApiView.as_view(), name='reviewapi'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='producdetailapi'),

    path('products/<str:slug>/tocart', ProductDetailPostView.as_view(), name='product-to-cart'),

    path('products/<str:slug>/review/', ReviewsForProductView.as_view(), name='reviewforproducdetailapi'),
    path('product/<slug>/questions/', QuestionListCreateAPIView.as_view(), name='question-list-create'),
    path('product/<slug>/questions/<int:question_id>/answer/', AnswerCreateAPIView.as_view(), name='answer-create'),
    path('productlist/', ProductListView.as_view(), name='productlist'),
    path('productlist-filter/', ProductToCategory.as_view(), name='product-filter'),
    path('categories/', CategoryListView.as_view(), name='category'),
    # path('categories/<str:slug>/', CategoryDetailView.as_view(), name='category'),

    path('variant/', VariantView.as_view(), name='variants'),

    path('cart/', CartGroupedView.as_view(), name='cart-grouped'),
    path('cart/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),

    path('drf-auth/', include('rest_framework.urls')),


    path('orders/', ListOrdersAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', RetrieveOrderAPIView.as_view(), name='order-detail'),
    path('orders/create/', CreateOrderAPIView.as_view(), name='order-create'),

    path('brands/', BrandView.as_view(), name='brands'),

    path('banners/', BannerView.as_view(), name='banner'),
    path('service/', ServiceView.as_view(), name='servise'),
    path('videos/', VideoView.as_view(), name='videos')



]