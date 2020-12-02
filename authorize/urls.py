from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
  path('shops/', views.ShopList.as_view(), name = 'shop-list'),
  path('shops/<int:pk>/', views.ShopDetail.as_view(), name = 'shop-detail'),
  path('shops/<int:pk>/add-product/', views.AddProduct.as_view(), name = 'add-product'),
  #path('api-root/', views.api_root),
  #path('users/', views.UserViewSet.as_view(), name = 'user-list'),
   path('users/', views.UserList.as_view(), name = 'user-list'),
   path('users/<int:pk>/', views.UserDetail.as_view(), name = 'user-detail'),
   path('', views.api_root),


  ]

urlpatterns = format_suffix_patterns(urlpatterns)
