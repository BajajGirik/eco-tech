from rest_framework import generics
from .serializers import UserSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    response_format = {
        "success_message": "Account created successfully. Please login to continue",
        "error_message": "Account creation failed",
        "success_data_key": "user",
        "error_data_key": "error",
    }
