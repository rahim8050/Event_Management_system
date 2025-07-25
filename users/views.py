# users/views.py

from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        # Use RegisterSerializer for both create and our custom register action:
        if self.action in ("create", "register"):
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
        # Allow anyone to hit both create (POST /api/users/) and register (POST /api/users/register/)
        if self.action in ("create", "register"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="register",
    )
    def register(self, request):
        """
        POST /api/users/register/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"status": "password changed"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], permission_classes=[permissions.IsAuthenticated], url_path="delete_me")
    def delete_me(self, request):
        request.user.delete()
        return Response({"status": "user deleted"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get", "put", "patch"], permission_classes=[permissions.IsAuthenticated], url_path="profile")
    def profile(self, request):
        user = request.user
        if request.method == "GET":
            return Response(UserSerializer(user).data)
        partial = request.method == "PATCH"
        serializer = UserSerializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"user": serializer.data, "message": "profile updated"})


class LoginView(generics.GenericAPIView):
    """
    POST /login/  → returns JWT tokens
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "user": {"id": user.id, "email": user.email},
            },
            status=status.HTTP_200_OK,
        )