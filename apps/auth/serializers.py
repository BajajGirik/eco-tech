from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

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
