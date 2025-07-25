"""
URL configuration for Api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db import router
from django.shortcuts import redirect

from rest_framework.authtoken.views import obtain_auth_token
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from users.views import UserViewSet, LoginView  # Correct import path

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/delete/<int:pko>/', UserViewSet.as_view({'delete': 'destroy'})),
    # Redirect root to API documentation
    path('', lambda request: redirect('api/')),

    # API endpoints
    path('api/', include(router.urls)),

    # path('api/users/delete/<int:pk>/', UserViewSet.as_view({'delete': 'destroy'}),

    path('api-auth/', include('rest_framework.urls')),
    # path('users/delete/<int:username_id>/', UserDetailView.as_view(), name='user-detail'),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/',LoginView.as_view(), name='login'),
]