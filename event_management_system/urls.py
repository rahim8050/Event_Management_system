# event_management_system/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserViewSet, LoginView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('api/')),
    path('api/users/', include('users.urls')),
    path('api/users/login/', LoginView.as_view(), name='login'),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
