from django.urls import path
from .views import RegisterAPIView

# App's namespace
app_name = "auth"

urlpatterns = [
    path("", RegisterAPIView.as_view(), name="register"),
]
