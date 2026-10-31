from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsMe
from .serializers import CreateUserSerializer, ResponseUserSerializer, UpdateUserSerializer

User = get_user_model()


class ListCreateUser(generics.ListCreateAPIView):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ResponseUserSerializer
        return CreateUserSerializer

class DetailUser(generics.RetrieveUpdateAPIView):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    queryset = User.objects.all()
    permission_classes = [IsMe]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ResponseUserSerializer
        return UpdateUserSerializer

class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(ResponseUserSerializer(request.user).data, status=200)