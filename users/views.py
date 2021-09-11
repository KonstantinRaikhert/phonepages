from django.shortcuts import get_object_or_404
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import AdvancedUser

from .serializers import CreateUserSerializer, TokenSerializer, UserSerializer


class TokenAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        methods=["post"],
        request_body=TokenSerializer,
        responses={
            201: "{ auth_token: token }",
        },
    )
    @action(detail=False, methods=["post"])
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "auth_token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        methods=["post"],
        responses={
            201: "{ message: The user has logged out }",
        },
    )
    @action(detail=False, methods=["post"])
    def post(self, request):
        token = get_object_or_404(Token, user=request.user)
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = AdvancedUser.objects.all()

    def get_serializer_class(self):
        if self.action != "list" and self.action != "retrieve":
            return CreateUserSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        url_path="me",
        url_name="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def view_me(self, request):
        user = get_object_or_404(AdvancedUser, username=request.user.username)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid() and request.method == "PATCH":
            serializer.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
