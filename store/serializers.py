from .models import *
from customer.models import *
from usauth.models import *
from vendor.models import *
from hitcount.models import HitCount
from rest_framework.serializers import ValidationError, SlugRelatedField, PrimaryKeyRelatedField, DecimalField, IntegerField, ModelSerializer, SerializerMethodField,CharField, DateTimeField, ReadOnlyField

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price']

class ReviewForProductSerializer(ModelSerializer):
    user_name = SerializerMethodField()
    product_name = SerializerMethodField()
    image_user=SerializerMethodField()

    class Meta:
        model = Review
        fields = ['user_name', 'image_user', 'product_name', 'rating', 'review']

    def get_image_user(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.image.url if profile.image else None
        except Profile.DoesNotExist:
            return None

    def get_user_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.full_name
        except Profile.DoesNotExist:
            return obj.user.username

    def get_product_name(self, obj):
        if obj.product:
            return obj.product.name
        return "Product not available"


#ProducDetailSerializer

class ProductDetailSerializer(ModelSerializer):
    new_rating = SerializerMethodField()
    review_count = SerializerMethodField()
    # variant = SerializerMethodField()
    vendor_name=SerializerMethodField()
    discount_percentage=SerializerMethodField()
    media=SerializerMethodField()
    reviews=SerializerMethodField()
    hitcount=SerializerMethodField()
    # currency=SerializerMethodField()
    similar_products=SerializerMethodField()
    viewed_products=SerializerMethodField()
    price_variant=SerializerMethodField()


    class Meta:
        model = Product
        fields = [
            'name', 'image', 'media', 'description', 'additional_info', 'new_rating',
            'review_count', 'price_variant', 'discount_percentage', 'vendor_name', 'reviews', 'hitcount',
            'similar_products', 'viewed_products',
        ]


    def get_regular_price(self, obj):
        if obj.on_sale:
            return obj.regular_price
        return None

    def get_new_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews) / reviews.count()
            return round(total_rating)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.count()


    def get_vendor_name(self, obj):
        vendor = Vendor.objects.filter(user=obj.vendor).first()
        if vendor:
            return vendor.store_name
        return None

    def get_discount_percentage(self, obj):
        if obj.regular_price and obj.price and obj.regular_price > obj.price:
            discount = ((obj.regular_price - obj.price) / obj.regular_price) * 100
            return round(discount)
        return 0

    def get_media(self, obj):
        media_items = Media.objects.filter(product=obj)
        media_images = [media.image.url for media in media_items]
        return media_images

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        reviews_data=ReviewForProductSerializer(reviews, many=True).data
        review_count=len(reviews_data)

        return {
            'count': review_count,
            'reviews': reviews_data
        }

    def get_hitcount(self, obj):
        hit_count = HitCount.objects.get_for_object(obj)

        return hit_count.hits

    def get_similar_products(self, obj):
        similar_products = Product.objects.filter(category=obj.category).exclude(id=obj.id)[:5]
        return [
            {
                'photo': product.image.url if product.image else None,
                'name': product.name,
                'price_variant': self.get_price_variant(product),
            }
            for product in similar_products
        ]

    def get_viewed_products(self, obj):
        viewed_products = HitCount.objects.filter(content_type__model='product').order_by('-hits')[:5]
        # print(viewed_products)
        viewed_products_data = []
        for hit in viewed_products:
            product = hit.content_object
            if isinstance(product, Product):
                viewed_products_data.append({
                    'photo': product.image.url if product.image else None,
                    'name': product.name,
                    'price_variant': self.get_price_variant(product)
                })
        return viewed_products_data


    def get_price_variant(self, obj):
        user = self.context.get('user')
        variant = Variant.objects.filter(product=obj).first()

        if variant:
            return variant.price_variant(user) if user else variant.price_variant_field

        return obj.price



class ProductReviewSerializer(ModelSerializer):
    user_name = SerializerMethodField()
    product_name = SerializerMethodField()
    image_user = SerializerMethodField()
    date = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Review
        fields = ['user_name', 'product_name', 'image_user', 'rating', 'review', 'date']

    def get_image_user(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.image.url if profile.image else None
        except Profile.DoesNotExist:
            return None

    def get_user_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.full_name
        except Profile.DoesNotExist:
            return obj.user.username

    def get_product_name(self, obj):
        return obj.product.name






class AnswerSerializer(ModelSerializer):
    user_name =SerializerMethodField()
    date_answered = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    answer_text = CharField()

    class Meta:
        model = Answer
        fields = ['user_name', 'answer_text', 'date_answered']

    def get_user_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.full_name
        except Profile.DoesNotExist:
            return obj.user.username

class QuestionSerializer(ModelSerializer):
    user_name = SerializerMethodField()
    product_name = CharField(source='product.name', read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    answer_count=SerializerMethodField()

    class Meta:
        model = Question
        fields = ['user_name', 'product_name', 'question_text', 'date_asked', 'answers', 'answer_count']

    def get_user_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.full_name
        except Profile.DoesNotExist:
            return obj.user.username


    def get_answer_count(self, obj):
        return obj.answers.count()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if not response.get('answers'):
            response['answers'] = []
        return response



##Productlist-filter
class ProductListSerializer(ModelSerializer):
    new_rating = SerializerMethodField()
    discount_percentage = SerializerMethodField()
    price_variant=SerializerMethodField()
    # currency = SerializerMethodField()


    class Meta:
        model = Product
        fields = [
            'name', 'image', 'new_rating', 'price_variant',
            'discount_percentage',
        ]

    def get_price_variant(self, obj):
        user = self.context.get('user')
        variant = Variant.objects.filter(product=obj).first()

        if variant:
            return variant.price_variant(user) if user else variant.price_variant_field

        return obj.price

    def get_new_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews) / reviews.count()
            return round(total_rating)
        return 0

    def get_discount_percentage(self, obj):
        if obj.regular_price and obj.price and obj.regular_price > obj.price:
            discount = ((obj.regular_price - obj.price) / obj.regular_price) * 100
            return round(discount)
        return 0



class CategorySerializer(ModelSerializer):

    class Meta:
        model=Category
        fields=['title', 'image', 'parent']


class BrandSerializer(ModelSerializer):
    class Meta:
        model=Brand
        fields=['brand_name', 'image']

class BannerSerializer(ModelSerializer):
    class Meta:
        model=Banners
        fields=['title','description', 'image', 'link']


class VideoSerializer(ModelSerializer):
    class Meta:
        model=Videos
        fields=['title','description', 'video', 'link']

class ServiseSerializer(ModelSerializer):
    class Meta:
        model=Service
        fields=['title', 'icon', 'subtitle']



class ColorSerializer(ModelSerializer):
    class Meta:
        model=Color
        fields='__all__'

class SizeSerializer(ModelSerializer):
    class Meta:
        model=Size
        fields='__all__'


class StyleSerializer(ModelSerializer):
    class Meta:
        model=Style
        fields='__all__'



##CART ORDER <<<<<------->>>>>








class CartItemSerializer(ModelSerializer):
    product_name = CharField(source='product.name', read_only=True)
    product_price = DecimalField(source='product.price', max_digits=15, decimal_places=2, read_only=True)
    price_variant=SerializerMethodField()
    # product_vendor = CharField(source='product.vendor.store_name', read_only=True)
    product_vendor=SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_vendor', 'variant', 'product_name', 'product_price','price_variant', 'qty', 'created_at', 'total_price',
                  'updated_at']
        read_only_fields = ['cart','product_vendor','created_at', 'price_variant', 'updated_at']

    def get_product_vendor(self, obj):
        if obj.product.vendor and hasattr(obj.product.vendor, 'vendor'):
            return obj.product.vendor.vendor.store_name
        return "Нет информации о продавце"

    def get_price_variant(self, obj):
        user = self.context.get('user')
        if obj.variant and obj.variant.price_variant() is not None:
            return obj.variant.price_variant(user) if user else obj.variant.price_variant_field
        return obj.product.price

    def validate(self, data):
        user = self.context.get('request').user
        cart = data.get('cart')
        product = data.get('product')
        variant=data.get('variant')

        if variant:
            if CartItem.objects.filter(cart=cart, product=product, variant=variant).exists():
                raise ValidationError("Этот товар с выбранным вариантом уже в вашей корзине.")
        else:
            if CartItem.objects.filter(cart=cart, product=product, variant__isnull=True).exists():
                raise ValidationError("Этот товар без варианта уже в вашей корзине.")

        return data



class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = ReadOnlyField()
    total_price = ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'created_at', 'updated_at', 'total_items', 'total_price', 'items']



class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'qty', 'variant', 'price', 'subtotal_price',
            'initial_total', 'saved', 'coupon',
            'applied_coupon', 'item_id', 'vendor', 'date'
        ]


class OrderSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    address=SerializerMethodField()
    # cart=SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'customer',
            'total', 'payment_method', 'payment_status', 'order_status',
            'address', 'coupons', 'payment_id', 'date', 'order_items'
        ]
        read_only_fields=['order_id', 'subtotal_price', 'customer',
            'total',  'payment_status', 'order_status',
            'address', 'coupons', 'payment_id', 'date', 'order_items']

    def get_address(self, obj):
        if obj.address:
            return {
                'full_name': obj.address.full_name,
                'mobile': obj.address.mobile,
                'country': obj.address.country,
                'state': obj.address.state,
                'city': obj.address.city,
                'address': obj.address.address,
                'zip_code': obj.address.zip_code
            }
        return None
#






