from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name", "avatar"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, password):
        validate_password(password); return password

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ResponseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "avatar", "date_joined"]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "avatar"]