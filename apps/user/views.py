from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsMe
from .serializers import CreateUserSerializer, ResponseUserSerializer
User = get_user_model()


class ListCreateUser(generics.ListCreateAPIView):
    parser_class = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return [ResponseUserSerializer]
        return [CreateUserSerializer]

class DetailUser(generics.RetrieveUpdateAPIView):
    parser_class = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    queryset = User.objects.all()
    serializer_class = ResponseUserSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [IsMe()]

class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(ResponseUserSerializer(request.user).data, status=200)