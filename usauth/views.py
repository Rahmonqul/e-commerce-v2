from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

# class RegisterUserAPIView(CreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def perform_create(self, serializer):
#         serializer.save()
#
#     def get_queryset(self):
#         return User.objects.all()
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserSerializer

class RegisterUserAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        self.response_data = {
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(self.response_data, status=status.HTTP_201_CREATED)


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProfileSerializer

    def get_object(self):

        if not self.request.user.is_authenticated:
            raise NotFound("Profile not found. Please register or log in.")
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=self.request.user)
        return profile

