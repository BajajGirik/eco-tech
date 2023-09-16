from rest_framework import generics
from .serializers import LoginSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    response_format = {
        "success_message": "Account created successfully. Please login to continue",
        "error_message": "Account creation failed",
        "success_data_key": "user",
        "error_data_key": "error",
    }

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    response_format = {
        "success_message": "Login successful",
        "error_message": "Login failed. Please try again",
        "success_data_key": "tokens",
        "error_data_key": "error",
    }
