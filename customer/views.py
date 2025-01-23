from rest_framework import generics
from .models import Address, Whishlist
from usauth.models import Profile
from .serializers import AddressSerializer, WhishlistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.sessions.models import Session

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


import uuid
from rest_framework.exceptions import ValidationError

class WhishlistView(generics.ListCreateAPIView):
    queryset = Whishlist.objects.all()
    serializer_class = WhishlistSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        if self.request.user.is_authenticated:
            return Whishlist.objects.filter(user=self.request.user)
        else:
            session_id = self.request.session.session_key
            if not session_id:
                self.request.session.create()
                session_id = self.request.session.session_key

            try:
                uuid.UUID(session_id)
            except ValueError:

                session_id = str(uuid.uuid4())
                self.request.session['session_key'] = session_id
                self.request.session.save()

            return Whishlist.objects.filter(session_id=session_id)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            session_id = self.request.session.session_key
            if not session_id:
                self.request.session.create()
                session_id = self.request.session.session_key

            try:
                uuid.UUID(session_id)
            except ValueError:

                session_id = str(uuid.uuid4())
                self.request.session['session_key'] = session_id
                self.request.session.save()

            serializer.save(session_id=session_id)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        if not product_id:
            return Response({"detail": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            exists = Whishlist.objects.filter(user=request.user, product_id=product_id).exists()
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key

            try:
                uuid.UUID(session_id)
            except ValueError:

                session_id = str(uuid.uuid4())
                request.session['session_key'] = session_id
                request.session.save()

            exists = Whishlist.objects.filter(session_id=session_id, product_id=product_id).exists()

        if exists:
            return Response({"detail": "Product is already in wishlist."}, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)








class RemoveProductFromWhishlist(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, product_id, *args, **kwargs):
        if request.user.is_authenticated:
            whishlist_item = Whishlist.objects.filter(user=request.user, product_id=product_id).first()
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            whishlist_item = Whishlist.objects.filter(session_id=session_id, product_id=product_id).first()

        if not whishlist_item:
            return Response({"detail": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)

        whishlist_item.delete()
        return Response({"detail": "Product removed from wishlist."}, status=status.HTTP_204_NO_CONTENT)
