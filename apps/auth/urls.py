from django.urls import path
from .views import LoginAPIView, RegisterAPIView

# App's namespace
app_name = "auth"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
]
