from rest_framework import serializers
from apps.user.serializers import ResponseUserSerializer
from .models import Art

class ArtSerializer(serializers.ModelSerializer):
    user = ResponseUserSerializer(read_only=True)
    class Meta:
        model = Art
        fields = "__all__"