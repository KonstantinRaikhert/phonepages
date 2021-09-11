from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from users.models import AdvancedUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedUser
        fields = [
            "id",
            "username",
            "last_name",
            "first_name",
            "email",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = AdvancedUser
        fields = [
            "id",
            "username",
            "last_name",
            "first_name",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = AdvancedUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate(self, data):
        email = data["email"]
        password = data["password"]
        if email is None:
            raise serializers.ValidationError(_("Введите email."))
        if password is None:
            raise serializers.ValidationError(_("Введите пароль."))
        user = authenticate(username=email, password=password)
        print(user)
        if user is None:
            raise serializers.ValidationError(
                _("Пользователь с таким email или паролем не найден.")
            )

        if not user.is_active:
            raise serializers.ValidationError(_("Пользователь заблокирован."))

        return user
