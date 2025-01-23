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
        read_only_fields=['user']
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

    def update(self, instance, validated_data):
        """
        Allow users to update their existing address.
        """
        instance.country = validated_data.get('country', instance.country)
        instance.state = validated_data.get('state', instance.state)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.save()
        return instance
