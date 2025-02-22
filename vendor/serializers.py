from .models import *
from customer.models import *
from usauth.models import *
from vendor.models import *
from store.serializers import ProductListSerializer

from rest_framework.serializers import ModelSerializer, SerializerMethodField,CharField, DateTimeField

class VendorsSerializer(ModelSerializer):
    review_count=SerializerMethodField()
    new_rating=SerializerMethodField()
    class Meta:
        model = Vendor
        fields = ['store_name', 'image', 'review_count', 'new_rating']

    def get_new_rating(self, obj):
        reviews = obj.storereviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews) / reviews.count()
            return round(total_rating)
        return 0

    def get_review_count(self, obj):
        return obj.storereviews.count()

class VendorDetailSerializer(ModelSerializer):
    review_count=SerializerMethodField()
    new_rating=SerializerMethodField()
    date = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    phone_number=SerializerMethodField()
    # productlist=SerializerMethodField()


    class Meta:
        model = Vendor
        fields = ['store_name', 'image', 'description', 'review_count', 'new_rating', 'date', 'phone_number']

    def get_new_rating(self, obj):
        reviews = obj.storereviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews) / reviews.count()
            return round(total_rating)
        return 0

    def get_review_count(self, obj):
        return obj.storereviews.count()

    def get_phone_number(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.mobile
        except Profile.DoesNotExist:
            return None

    # def get_productlist(self, obj):
    #     products = Product.objects.filter(vendor=obj.user)
    #     return ProductListSerializer(products, many=True).data

class ReviewForStoreSerializer(ModelSerializer):
    user_name = SerializerMethodField()
    image_user=SerializerMethodField()

    class Meta:
        model = StoreReview
        fields = ['user_name', 'image_user','rating', 'review', 'reply', 'date']
        read_only_fields=['reply','date']
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

