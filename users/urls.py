# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, LoginView

router = DefaultRouter()
# This registers ALL your UserViewSet actions at /api/users/...
router.register("", UserViewSet, basename="user")

urlpatterns = [
   
    path("", include(router.urls)),

    # Login endpoint (public)
    path("login/", LoginView.as_view(), name="login"),

    # JWT refresh (public)
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
