from rest_framework import status
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView,DestroyAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import Product, Review,Question, Answer, Category
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import django_filters
from .filters import ProductFilter, ProductListFilter
from hitcount.views import HitCountDetailView
from rest_framework.decorators import api_view
from django.db import transaction
from decimal import Decimal
from django.db.models import OuterRef, Subquery
from django.db.models import Prefetch


# ProductAPi Продукты GET
class ProductApiView(APIView):
    category_choices = openapi.Parameter(
        'category',
        openapi.IN_QUERY,
        description="Filter products by category",
        type=openapi.TYPE_STRING,
        enum=['best_sellers', 'new_arrivals', 'sale']
    )


    page_param = openapi.Parameter(
        'page',
        openapi.IN_QUERY,
        description="Page number for pagination",
        type=openapi.TYPE_INTEGER,
        default=1
    )
    page_size_param = openapi.Parameter(
        'page_size',
        openapi.IN_QUERY,
        description="Number of items per page",
        type=openapi.TYPE_INTEGER,
        default=10
    )

    @swagger_auto_schema(manual_parameters=[category_choices, page_param, page_size_param])
    def get(self, request, *args, **kwargs):
        try:
            category = request.GET.get('category', None)

            if category == 'best_sellers':
                products = Product.objects.filter(best_seller=True)
            elif category == 'new_arrivals':
                products = Product.objects.filter(new_arrival=True)
            elif category == 'sale':
                products = Product.objects.filter(sale=True)
            else:
                products = Product.objects.all()

            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)

            paginator = Paginator(products, page_size)
            try:
                products_page = paginator.page(page)
            except PageNotAnInteger:
                products_page = paginator.page(1)
            except EmptyPage:
                products_page = paginator.page(paginator.num_pages)

            serializer = ProductSerializer(products_page, many=True)

            return Response({
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'results': serializer.data
            })
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#Rview отзывы GET
class ReviewApiView(ListAPIView):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(active=True)


#ProductDetail GET

class ProductDetailView(RetrieveAPIView, HitCountDetailView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    count_hit = True

    permission_classes = [AllowAny]

    def get_queryset(self):
        return super().get_queryset()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context


class ReviewsForProductView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductReviewSerializer

    class Pagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    pagination_class = Pagination

    def get_product(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

    def get_queryset(self):
        slug = self.kwargs['slug']
        product = self.get_product(slug)
        return product.reviews.all()

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        product = self.get_product(slug)
        serializer.save(user=self.request.user, product=product)




class QuestionListCreateAPIView(ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_product(self, slug):
        return get_object_or_404(Product, slug=slug)

    def get_queryset(self):
        slug = self.kwargs['slug']
        product = self.get_product(slug)
        return product.questions.all()

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        product = self.get_product(slug)
        serializer.save(user=self.request.user, product=product)


class AnswerCreateAPIView(CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_question(self, question_id):
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        question = get_object_or_404(Question, id=question_id, product=product)
        return question

    def get(self, request, slug, question_id, *args, **kwargs):
        question = self.get_question(question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def perform_create(self, serializer):
        question = self.get_question(self.kwargs['question_id'])
        serializer.save(user=self.request.user, question=question)

    def post(self, request, *args, **kwargs):
        question = self.get_question(self.kwargs['question_id'])

        if not question.active:
            return Response({"detail": "Этот вопрос больше не активен."}, status=status.HTTP_400_BAD_REQUEST)

        response = super().post(request, *args, **kwargs)

        question = self.get_question(self.kwargs['question_id'])
        question_serializer = QuestionSerializer(question)

        return Response(question_serializer.data, status=status.HTTP_201_CREATED)


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class=ProductListFilter
    search_fields = ['name', 'category__title', 'subcategory__title']
    pagination_class = ProductPagination
    permission_classes = [AllowAny]
    def get_queryset(self):
        return super().get_queryset()


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context




class ProductToCategory(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [AllowAny]


    class Pagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    pagination_class = Pagination
    filterset_class = ProductFilter
    def get_queryset(self):
        queryset = super().get_queryset()
        variant_title = self.request.query_params.get('variant_title', None)
        if variant_title:
            queryset = queryset.filter(variant__variant_items__title__icontains=variant_title)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context

    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#
#
class BrandView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class BannerView(ListAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannerSerializer

    class BannerPagination(PageNumberPagination):
        page_size = 1

    pagination_class = BannerPagination

    def get_queryset(self):
        active_instance = Banners.objects.filter(is_active=True).first()
        all_banners = Banners.objects.all()

        if active_instance:
            banners = [active_instance] + list(all_banners.exclude(id=active_instance.id))
        else:
            banners = all_banners

        return banners

class VideoView(APIView):
    def get(self, request):
        active_instance = Videos.objects.filter(is_active=True).first()
        if active_instance:
            serializer = VideoSerializer(active_instance)
            return Response(serializer.data)
        return Response({"detail": "No active instance found"}, status=404)

class ServiceView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiseSerializer
    class ServicePagination(PageNumberPagination):
        page_size = 4

    pagination_class = ServicePagination




class ColorListView(ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeListView(ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class StyleListView(ListAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer






#CART ORDER <<<<<------>>>>



class ProductDetailPostView(ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        else:
            session_key = self.request.session.session_key or str(uuid.uuid4())
            cart, created = Cart.objects.get_or_create(session_id=session_key, is_active=True)

        return cart.items.all()

    def perform_create(self, serializer):
        product_id=self.request.data.get('product')

        product= get_object_or_404(Product, id=product_id)
        variant = self.request.data.get('variant')

        if self.request.user.is_authenticated:
            cart = Cart.objects.get(user=self.request.user, is_active=True)
        else:
            session_key = self.request.session.session_key or str(uuid.uuid4())
            cart, created = Cart.objects.get_or_create(session_id=session_key, is_active=True)

        if CartItem.objects.filter(cart=cart, product=product, variant=variant).exists():
            raise ValidationError("Этот товар с выбранным вариантом уже в вашей корзине.")

        if variant is None and CartItem.objects.filter(cart=cart, product=product, variant__isnull=True).exists():
            raise ValidationError("Этот товар без варианта уже в вашей корзине.")

        serializer.save(cart=cart, product=product)




class CartDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        else:
            session_key = self.request.session.session_key or str(uuid.uuid4())
            cart, created = Cart.objects.get_or_create(session_id=session_key, is_active=True)
        return cart

    def patch(self, request, *args, **kwargs):
        cart = self.get_object()
        action = request.data.get('action')

        if action == 'clear':
            cart.clear()
            return Response({'status': 'Cart cleared'}, status=status.HTTP_200_OK)

        return super().patch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user'] = self.request.user
        return context



class CartItemDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user)
        else:
            session_key = self.request.session.session_key
            return CartItem.objects.filter(cart__session_id=session_key)

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response({"message": "Товар успешно удален из корзины."}, status=status.HTTP_204_NO_CONTENT)






#Order





class CreateOrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Создаем заказ
        customer = request.user
        subtotal_price = Decimal('0.00')
        total = Decimal('0.00')


        adress_data = Address.objects.filter(user=customer).first()
        if not adress_data:
            raise ValidationError("User does not have an address.")


        order = Order.objects.create(
            customer=customer,
            subtotal_price=subtotal_price,
            total=total,
            order_status='Pending',
            address=adress_data,
            date=timezone.now()
        )

        cart_items = CartItem.objects.filter(cart__user=customer, cart__is_active=True)

        if not cart_items.exists():
            raise ValidationError("Cart is empty, unable to create an order.")

        for cart in cart_items:
            price = cart.variant.price_variant(request.user) if cart.variant else cart.product.price
            order_item = OrderItem.objects.create(
                order=order,
                product=cart.product,
                qty=cart.qty,
                variant=cart.variant,
                price=price,
                subtotal_price=cart.total_price,
                initial_total=cart.total_price or Decimal('0.00'),
                saved=Decimal('0.00'),
                vendor=cart.product.vendor,
            )

            order_item.coupon.set(Coupon.objects.filter(vendor=cart.product.vendor))


            subtotal_price += cart.variant.price_variant()
            total += cart.total_price


        order.subtotal_price = subtotal_price
        order.total = total
        order.save()

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

####CART













































































































































































































































#
