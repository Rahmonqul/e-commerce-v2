from rest_framework import serializers
from .models import Address
from usauth.models import Profile
from rest_framework.serializers import SerializerMethodField
class AddressSerializer(serializers.ModelSerializer):
    full_name=SerializerMethodField()
    mobile=SerializerMethodField()
    class Meta:
        model = Address
        fields = ['id', 'user', 'full_name', 'mobile', 'country', 'state', 'city', 'address', 'zip_code']

    def get_full_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.full_name
        except Profile.DoesNotExist:
            return obj.user.username

    def get_mobile(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.mobile
        except Profile.DoesNotExist:
            return None
