from rest_framework import generics
from .models import Address
from usauth.models import Profile
from .serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated

class AddressListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        user = self.request.user
        profile = Profile.objects.filter(user=user).first()

        full_name = serializer.validated_data.get('full_name', None)
        mobile = serializer.validated_data.get('mobile', None)

        if not full_name and profile:
            full_name = profile.full_name
        if not mobile and profile:
            mobile = profile.mobile

        serializer.save(user=user, full_name=full_name, mobile=mobile)

class AddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Address.objects.filter(user=self.request.user)
