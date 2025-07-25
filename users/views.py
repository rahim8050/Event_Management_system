from rest_framework import viewsets, permissions, status, generics, request
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserCreateSerializer, PasswordChangeSerializer, UserLoginSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data.get('old_password')):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response({"status": "password changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_me(self, request):
        user = request.user
        user.delete()
        return Response({"status": " user deleted successfully"}, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user

        if request.method == 'GET':
            # View profile
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            # Update profile
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(user, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'user': serializer.data,
                'message': 'Profile updated successfully'
            })


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'success',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)


