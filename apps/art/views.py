from rest_framework import generics, permissions, parsers
from rest_framework.response import Response

from apps.user.permissions import IsMine
from .models import Art
from .serializers import ArtSerializer

class ListCreateArt(generics.ListCreateAPIView):
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    queryset = Art.objects.all()
    serializer_class = ArtSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=self.request.user)
        return Response(serializer.data, status=201)

class DetailArt(generics.RetrieveUpdateAPIView):
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    queryset = Art.objects.all()
    serializer_class = ArtSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [IsMine()]