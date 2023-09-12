from rest_framework import generics
from .serializers import UserSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
