from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length = 200, db_index = True, unique = True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Shop(models.Model):
    shop_name = models.CharField(max_length = 255, blank = True, default = '')
    owner = models.ForeignKey('auth.user', related_name = 'shops', on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category)
    delivery_time = models.CharField(max_length = 70, blank = True, default = '40 min')
    discount_coupon = models.CharField(max_length = 128, blank = True, default = 'new_shop')
    rating = models.FloatField(default = 0,validators = [MaxValueValidator(5), MinValueValidator(0)])

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.shop_name



class Product(models.Model):
    #category = models.ForeignKey(Category, related_name = 'products', on_delete = models.CASCADE)
    name = models.CharField(max_length = 255, blank = True, db_index = True)
    slug = models.SlugField(max_length = 255, db_index = True, blank = True)
    image = models.ImageField(upload_to = 'products/%Y/%m/%d', blank = True)
    price = models.DecimalField(max_digits= 10, decimal_places = 2)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'products', default = '', null = True, blank = True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
