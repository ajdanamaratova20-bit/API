from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

from .serializers import UserSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Получить профиль текущего пользователя',
        responses=UserSerializer,
        tags=['Пользователь'],
    )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)