"""EasyForLazy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from authorize import views
from rest_framework import routers
from knox import views as knox_views
from rest_framework.urlpatterns import format_suffix_patterns

#router = routers.DefaultRouter()
#router.register(r'users',views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/register/',views.RegisterAPI.as_view(),name = 'register'),
    #path('users/',views.UserList.as_view(), name = 'user-list'),
    #path('users/<int:pk>/', views.UserDetail.as_view(), name = 'user-detail'),
    #path('',include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
    path('', include('authorize.urls')),

    path('api/login/', views.LoginAPI.as_view(), name = 'login'),
    #path('api/logout/', knox_views.LogoutView.as_view(),name = 'logout'),
    #path('api/logoutall/',knox_views.LogoutAllView.as_view(), name = 'logoutall'),
    #path('api/change-password/', views.ChangePasswordView.as_view(), name = 'change-password'),


]
