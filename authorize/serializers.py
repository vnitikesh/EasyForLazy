from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Shop, Product, Review
from rest_framework.fields import CurrentUserDefault

# The RegisterSerializer class is the subclass of ModelSerializer and is doing the work of deserialization of input requests and serialization of output response.
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    # Defining --> the seialization is based upon User model with the following field attributes and extra_kwargs to set extra functionality to password field.
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password':{'write_only': True}}


    # Validation of password and confirm_password is done over here when serializer.is_valid() is called in view function
    def validate_password(self, password):
        if(password != self.initial_data['confirm_password']): # Here the statement is checking whether the intended password is not equal to confirm_password
            print("Validation not passed")
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        print("Validation Passed")


    # create method is inherited from ModelSerializer which is called or run when the user is being created i.e. when serializer.save() is called in view function
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['confirm_password'])
        return user # This function is returning the user object after successful registration and creation of User.


# UserSerializer is inherited from HyperlinkedModelSerializer and serializing and deserializing the User related requests and forwarding the response.
class UserSerializer(serializers.HyperlinkedModelSerializer):

    shops = serializers.HyperlinkedRelatedField(many = True, view_name = 'shop-detail', read_only = True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'shops') # These fields would be serialized and forwarding the response


# The class is inherited from SlugRelatedField  and is acting as a helper for ProductSerializer's shop attribute
class SlugRelatedModuleField(serializers.SlugRelatedField):

    # Customized queryset which is sending GET response in the form of shop object filterised by the user in session.
    def get_queryset(self):
        queryset = Shop.objects.all()
        request = self.context.get('request', None)
        queryset = queryset.filter(owner = request.user)
        return queryset


# This ProductSerializer class inherited from ModelSerializer is harnessing the Product model class and its fields to serialize the info.
class ProductSerializer(serializers.ModelSerializer):

    shop = SlugRelatedModuleField(slug_field = 'shop_name') # Here the shop attribute is calling SlugRelatedModuleField with its parameters set to slug_field attribute which will display the shop_name

    # Meta class is defining the Product model and its tuple of fields to be harnessed.
    class Meta:
        model = Product
        fields = ('url', 'id', 'name', 'price', 'available', 'shop')


# ShopSerializer is inherited from HyperlinkedModelSerializer and include two extra field attributes
class ShopSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username') # owner attribute is ReadOnlyField and is serializing the shop owner's username
    products = ProductSerializer(many = True, read_only = True) # products attribute is encapsulating the ProductSerializer and is intended to throw read_only multiple product objects.

    # Meta class is including the model and fields attributes which depicts the models and fields to be processed for serialization activity.
    class Meta:
        model = Shop
        fields = ('url', 'id', 'shop_name', 'owner', 'delivery_time', 'discount_coupon', 'rating', 'products')


# The ReviewSerializer inherited from serializers.ModelSerializer is processing and throwing the serialized request/response regarding the Review related objects.
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username') # Here we are associating user ReadOnlyField to depict the review related to particular user.

    class Meta:
        model = Review
        fields = ('user', 'date', 'rating', 'comment')

'''
class CartSerializer(serializers.ModelSerializer):
    created_by = serializers.CurrentUserDefault()
    class Meta:
        model = Cart
        fields = [
        'created_by','order_items', 'subtotal', 'tax_percentage', 'tax_total', 'total',
        ]

'''
'''
class get_user:
    def __init__(self):
        user = None
        request = self.context.get("request")
        if(request and hasattr(request, "user")):
            user = request.user
'''
'''
class AttrPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Shop.objects.filter(owner = user)
        return queryset
'''
