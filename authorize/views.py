from django.shortcuts import render, get_object_or_404
from .serializers import UserSerializer, ShopSerializer, ProductSerializer, ReviewSerializer, RegisterSerializer
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .models import Shop, Product, Review
from .permissions import IsOwnerOrReadOnly, IsShopOrReadOnly
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

# Entry Point view which is accepting only GET requests set by @api_view() decorator.
@api_view(['GET'])
# The api_root() function contains the dictionary of links response which associates the api conncectivity to the outer world.
def api_root(request, format = None):
    return Response({
    'users': reverse('user-list', request = request, format = format),
    'shops': reverse('shop_list', request = request, format = format),
    'product-list': reverse('add-product', request = request, format = format),

    })

# The RegisterAPI view class is inherited from GenericAPIView parent class and utilizing the RegisterSerializer class set by serializer_class attribute.
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer


    # This method intends to handle the POST request
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data) # Returning a RegisterSerializer instance on posted data named by request.data in the data attribute.
        serializer.is_valid(raise_exception = True) # Validation checkup is done against the password meant to be set and confirm_password
        user = serializer.save()

        return Response({
        "user": UserSerializer(user, context = self.get_serializer_context()).data,

        })


# This view class is inherited from generics.ListAPIView with the queryset and serializer_class attribute is set and the generic view is intended to list the users.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


# UserDetail view class is intended to retrieve details of each user
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


# The ShopList generic class is intended to create and list the shop objects and is meant to permit only authenticated users to do so.
class ShopList(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly
    ]
    name = 'shop-list'

    # perform_create() method is intended to set the owner field of ShopSerializer class to the current user in session
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


# Shop Detail view class is intended to handle GET and PUT requests regarding Shop objects by harnessing ShopSerializer class
# and is meant to be permitted only for authenticated and owner of the shop and applied read only limit to non-owner.
class ShopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]
    name = 'shop-detail'


# This class is inherited from generics.ListCreateAPIView and is intended to create and list the data according to queryset and serializer_class attribute
# Only meant to be permitted for authenticated users and the particular shop.
class AddProduct(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly, IsShopOrReadOnly
    ]



# queryset and serializer_class is crafted for GET and PUT requests and permitted only for authenticated users and the associated shop.
class AddProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly, IsShopOrReadOnly
    ]


# The GiveReview class is intended to handle the creation  and listing of review objects and permitted only for authenticated users.
class GiveReview(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly
    ]

    # Overriding the get_queryset() method for filtering the Review objects according to the shop_id.
    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(shop_id = self.kwargs.get('pk'))

    # Overriding the perform_create() method and getting the shop object filterised by the id.
    def perform_create(self, serializer):
        shop_id = self.kwargs.get('pk')
        shop = Shop.objects.get(pk = shop_id)
        #request = self.context.get('request', None)
        try:
            shop_obj = get_object_or_404(Shop.objects, shop_name = shop.shop_name)
            user_obj = get_object_or_404(User.objects, username = self.request.user.username)
            serializer.save(shop = shop_obj, user = user_obj)
        except DoesNotExist:
            pass

'''
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



'''


'''
    def perform_create(self, serializer):
        shop_name = self.request.data.get('pk', None)
        print(shop_name)
        print("Hey")
        shop_obj = get_object_or_404(Shop.objects, shop_name = shop_name)
        serializer.save(shop = shop_obj)
'''
