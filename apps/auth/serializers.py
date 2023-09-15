from typing import Any, Dict
from rest_framework.serializers import EmailField, ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "email": {
                "allow_blank": False,
                "required": True,
                "validators": [UniqueValidator(queryset=User.objects.all())]
            },
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        user = User.objects.create(
          username=validated_data["email"],
          email=validated_data["email"],
          first_name=validated_data["first_name"],
          last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """
    Custom serializer accepting `email` & `password` as input rather than
    `username` & `password` which is used by default.

    Note: If `username` and `email` fields are storing different data, you will
    not be able to login as this serializer just passes down the `email` value
    as `username` for authenticating.
    """
    email = EmailField(label="Email Address")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # We are removing the `username` field that was set by `rest_framework_simplejwt`
        # as we are using the `email` field instead
        del self.fields[self.username_field]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        # Popping the email field and changing the attrs dictionary itself to
        # provide the exact structure / payload that is expected by the base class.
        email = attrs.pop("email", "")

        return super().validate({
            **attrs,
            self.username_field: email
        })
