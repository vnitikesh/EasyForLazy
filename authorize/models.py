from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Declaration of Shop model class for storing shop related credentials like ('shop_name', 'owner of the shop', 'any discount coverage', delivery time)
# and many more.
class Shop(models.Model):
    shop_name = models.CharField(max_length = 255, blank = True, default = '')
    owner = models.ForeignKey('auth.user', related_name = 'shops', on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    delivery_time = models.CharField(max_length = 70, blank = True, default = '40min')
    discount_coupon = models.CharField(max_length = 128, blank = True, default = 'new_shop')
    rating = models.FloatField(default = 0, validators = [MaxValueValidator(5), MinValueValidator(0)])

    # Here Meta class is defined which sets the ordering of the shop data according to their creation
    class Meta:
        ordering = ['created']
    # Name of the object will be self.shop_name
    def __str__(self):
        return self.shop_name

#Declaration of Product model class for storing product related information like (name, price, availability, the shop with which they are associated)
class Product(models.Model):

    name = models.CharField(max_length = 255, blank = True, db_index = True)
    image = models.ImageField(upload_to = 'products/%Y/%m/%d', blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'products', null = True, blank = True)#Foreign key to the shop model class

# Meta class is defining --> Product will be stacked by alphabetical manner
    class Meta:
        ordering = ['name']
    # Name of the object will be self.name
    def __str__(self):
        return self.name

# The Review model class is declaring the data associated with the shops feedback like (rating, comments, and the user object who sends the feeback)
class Review(models.Model):
    #shop_id = models.IntegerField()
    user = models.ForeignKey('auth.user', related_name = 'user_reviews', on_delete = models.CASCADE) #Foreign Key to the User model
    shop = models.ForeignKey(Shop, related_name = 'shop_reviews', on_delete = models.CASCADE) #Foreign Key to the shop model
    date = models.DateTimeField(auto_now_add = True)
    rating = models.FloatField(default = 0, validators = [MaxValueValidator(5), MinValueValidator(0)])
    comment = models.TextField()

    # Name of the object will be self.user.username
    def __str__(self):
        return self.user.username
'''
class Item(models.Model):
    name = models.CharField(max_length = 255)

class Cart(models.Model):
    created_by = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
    subtotal = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.00)
    tax_percentage = models.DecimalField(max_digits = 10, decimal_places = 5, default = 0.085)
    tax_total = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.00)
    total = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.00)
    order_items = models.ManyToManyField(Product)
    shop = models.ForeignKey(Shop, related_name = 'shop-cart', on_delete = models.CASCADE)
'''
