from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name = 'register'),
    path('users/', views.UserList.as_view(), name = 'user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name = 'user-detail'),
    path('shops/', views.ShopList.as_view(), name = 'shop_list'),
    path('shops/<int:pk>/', views.ShopDetail.as_view(), name = 'shop-detail'),
    path('add-product/', views.AddProduct.as_view(), name = 'add-product'),
    path('add-product/<int:pk>/', views.AddProductDetail.as_view(), name = 'product-detail'),
    path('shops/<int:pk>/review/', views.GiveReview.as_view(), name = 'give-review'),
    #path('shops/<int:shop_pk>/review/<int:pk>/', views.ReviewDetail.as_view(), name = 'review-detail'),
    path('', views.api_root),
]
