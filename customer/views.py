from rest_framework import generics
from .models import Address
from usauth.models import Profile
from .serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied, NotFound

class AddressListCreateAPIView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        user = self.request.user
        if Address.objects.filter(user=user).exists():
            raise ValidationError(
                "You already have an address. Please update the existing address instead of creating a new one.")

        profile = Profile.objects.filter(user=user).first()

        full_name = serializer.validated_data.get('full_name', None)
        mobile = serializer.validated_data.get('mobile', None)

        if not full_name and profile:
            full_name = profile.full_name
        if not mobile and profile:
            mobile = profile.mobile

        serializer.save(user=user, full_name=full_name, mobile=mobile)

class AddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Address.objects.filter(user=self.request.user)

    def get_object(self):

        try:
            obj = super().get_object()
            if obj.user != self.request.user:
                raise PermissionDenied("Вы не можете редактировать или удалять этот адрес.")
            return obj
        except Address.DoesNotExist:
            raise NotFound("Адрес не найден.")

    def perform_update(self, serializer):

        if Address.objects.filter(user=self.request.user).exclude(id=self.get_object().id).exists():
            raise PermissionDenied("Вы можете иметь только один адрес.")
        serializer.save(user=self.request.user)
