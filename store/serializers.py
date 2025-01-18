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



class ProductDetailSerializer(ModelSerializer):
    new_rating = SerializerMethodField()
    review_count = SerializerMethodField()
    variant = SerializerMethodField()
    vendor_name=SerializerMethodField()
    discount_percentage=SerializerMethodField()
    media=SerializerMethodField()
    reviews=SerializerMethodField()
    hitcount=SerializerMethodField()
    currency=SerializerMethodField()
    similar_products=SerializerMethodField()
    viewed_products=SerializerMethodField()

    price_in_requested_currency = SerializerMethodField()
    regular_price_in_requested_currency = SerializerMethodField()
    currency_in_requested=SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'name', 'image', 'media', 'description', 'additional_info', 'new_rating',
            'review_count', 'price','regular_price', 'currency', 'discount_percentage', 'variant', 'vendor_name', 'reviews', 'hitcount',
            'similar_products', 'viewed_products', 'price_in_requested_currency', 'regular_price_in_requested_currency',
            'currency_in_requested'
        ]




    def get_currency(self, obj):
        return obj.currency.code

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

    def get_variant(self, obj):
        variant_items = VariantItem.objects.filter(variant__product=obj)
        variant_data = {}
        for item in variant_items:
            variant_name = item.variant.name.lower()
            if variant_name not in variant_data:
                variant_data[variant_name] = []
            variant_data[variant_name].append(item.title)
        return {k: ', '.join(v) for k, v in variant_data.items()}

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
                'price': product.price,
                'regular_price': product.regular_price
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
                    'price': product.price
                })
        return viewed_products_data

    def get_price_in_requested_currency(self, obj):
        # Передача контекста для получения профиля пользователя
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            profile = user.profile if hasattr(user, 'profile') else None
            if profile and profile.currency:
                user_currency = profile.currency
                conversion_rate = obj.get_currency_conversion_rate(obj.currency, user_currency)
                return round(obj.price * conversion_rate, 2)
        return obj.price

    def get_regular_price_in_requested_currency(self, obj):
        # Передача контекста для получения профиля пользователя
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            profile = user.profile if hasattr(user, 'profile') else None
            if profile and profile.currency:
                user_currency = profile.currency
                conversion_rate = obj.get_currency_conversion_rate(obj.currency, user_currency)
                return round(obj.regular_price * conversion_rate, 2)
        return obj.regular_price

    def get_currency_in_requested(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            profile = user.profile if hasattr(user, 'profile') else None
            if profile and profile.currency:
                return profile.currency.code
        return obj.currency.code


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


class ProductListSerializer(ModelSerializer):
    new_rating = SerializerMethodField()
    discount_percentage = SerializerMethodField()
    currency = SerializerMethodField()
    price_in_requested_currency = SerializerMethodField()
    regular_price_in_requested_currency = SerializerMethodField()
    currency_in_requested=SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'name', 'image', 'new_rating', 'price', 'regular_price',
            'discount_percentage', 'currency', 'price_in_requested_currency', 'regular_price_in_requested_currency',
            'currency_in_requested'
        ]

    def get_currency(self, obj):
        return obj.currency.code

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

    def get_price_in_requested_currency(self, obj):
        # Передача контекста для получения профиля пользователя
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            profile = user.profile if hasattr(user, 'profile') else None
            if profile and profile.currency:
                user_currency = profile.currency
                conversion_rate = obj.get_currency_conversion_rate(obj.currency, user_currency)
                return round(obj.price * conversion_rate, 2)
        return obj.price

    def get_regular_price_in_requested_currency(self, obj):
        # Передача контекста для получения профиля пользователя
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            profile = user.profile if hasattr(user, 'profile') else None
            if profile and profile.currency:
                user_currency = profile.currency
                conversion_rate = obj.get_currency_conversion_rate(obj.currency, user_currency)
                return round(obj.regular_price * conversion_rate, 2)
        return obj.regular_price
    def get_currency_in_requested(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            profile = user.profile if hasattr(user, 'profile') else None
            if profile and profile.currency:
                return profile.currency.code
        return obj.currency.code
class VariantItemSerializer(ModelSerializer):
    class Meta:
        model = VariantItem
        fields = ['title', 'content']

class VariantSerializer(ModelSerializer):
    variant_items = SerializerMethodField()

    class Meta:
        model = Variant
        fields = ['name', 'variant_items']

    def get_variant_items(self, obj):
        # Группируем элементы VariantItem по имени варианта
        grouped_items = VariantItem.objects.filter(variant__name=obj.name)
        return VariantItemSerializer(grouped_items, many=True).data


class CategorySerializer(ModelSerializer):
    # subcategory=SerializerMethodField()
    class Meta:
        model=Category
        fields=['title', 'image', 'parent']

    # def get_subcategory(self, obj):
    #     subcategories = obj.subcategories.all()
    #     return [sub.title for sub in subcategories]




class CartProductSerializer(ModelSerializer):
    product_name = SerializerMethodField()
    store_name = SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['product', 'product_name', 'store_name', 'qty', 'subtotal_price', 'size', 'color', 'date']

    def get_product_name(self, obj):
        return obj.product.name if obj.product else None

    def get_store_name(self, obj):
        try:
            store = Vendor.objects.get(user=obj.product.vendor)
            return store.store_name
        except Vendor.DoesNotExist:
            return None

    def create(self, validated_data):
        product = validated_data.get('product')
        size = validated_data.get('size')
        color = validated_data.get('color')


        validated_data['size'] = size
        validated_data['color'] = color

        validated_data.pop('store_name', None)

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        user = self.context.get('request').user
        if not user.is_authenticated:
            cart_data = self.context.get('request').session.get('cart', [])
            representation = [{
                'product': item['product'],
                'qty': item['qty'],
                'subtotal_price': item['subtotal_price'],
                'product_name': item['product_name'],
                'store_name': item['store_name'],
            } for item in cart_data]

        return representation

    def validate_product(self, value):
        user = self.context.get('request').user


        if user.is_authenticated:
            if Cart.objects.filter(user=user, product=value).exists():
                raise ValidationError("Этот товар уже в вашей корзине.")
        else:

            cart_data = self.context.get('request').session.get('cart', [])
            if any(item['product'] == value.id for item in cart_data):
                raise ValidationError("Этот товар уже в вашей корзине.")

        return value




#proba



class NewReviewSerializer(ModelSerializer):
    full_name=SerializerMethodField()
    class Meta:
        model=Review
        fields=['id','full_name', 'product','review', 'rating']

    def get_full_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.full_name
        except Profile.DoesNotExist:
            return "Unknown User"



class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'qty', 'size', 'color', 'price', 'subtotal_price',
            'shipping', 'tax', 'service_fee', 'initial_total', 'saved', 'coupon',
            'applied_coupon', 'item_id', 'vendor', 'date'
        ]

class OrderSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    adress=SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'customer', 'subtotal_price', 'shipping', 'tax', 'service_fee',
            'total', 'payment_method', 'payment_status', 'order_status', 'initial_total', 'saved',
            'adress', 'coupons', 'payment_id', 'date', 'order_items'
        ]


    def get_adress(self, obj):
        if obj.adress:
            return {
                'full_name': obj.adress.full_name,
                'mobile': obj.adress.mobile,
                'country': obj.adress.country,
                'state': obj.adress.state,
                'city': obj.adress.city,
                'address': obj.adress.address,
                'zip_code': obj.adress.zip_code
            }
        return None  # Если адрес отсутствует




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



