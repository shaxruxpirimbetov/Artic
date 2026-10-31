from rest_framework import serializers
from apps.user.serializers import ResponseUserSerializer
from apps.art.models import Art
from apps.art.serializers import ArtSerializer
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = ResponseUserSerializer(read_only=True)
    art = serializers.PrimaryKeyRelatedField(queryset=Art.objects.all(), write_only=True)
    art_detail = ArtSerializer(source="art", read_only=True)
    class Meta:
        model = Comment
        fields = ["user", "art_detail", "art", "content"]