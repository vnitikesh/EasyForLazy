from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Shop, Category, Product

#User Serializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
    shops = serializers.HyperlinkedRelatedField(many = True, view_name = 'shop-detail', read_only = True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'shops')

#Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

#Change-Password Serializer
class ChangePasswordSerializer(serializers.Serializer):
    class Meta:

        model = User

        old_password = serializers.CharField(required = True)
        new_password = serializers.CharField(required = True)

class CategorySerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.name
    class Meta:
        model = Category

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    products = serializers.HyperlinkedRelatedField(many = True, view_name = 'add-product', read_only = True)
    #category = CategorySerializer(read_only = True, many = True)
    class Meta:
        model = Shop
        fields = ['id', 'shop_name', 'owner', 'delivery_time','discount_coupon','rating', 'products']



class ShopDetailSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    category = CategorySerializer(read_only = True, many = True)
    products = serializers.HyperlinkedRelatedField(many = True, view_name = 'add-product', read_only = True)
    class Meta:
        model = Shop
        fields = ('id', 'shop_name', 'owner', 'category', 'delivery_time', 'discount_coupon', 'rating', 'products')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    shop_owner = serializers.ReadOnlyField(source = 'shop.shop_name')
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'available', 'shop_owner')
