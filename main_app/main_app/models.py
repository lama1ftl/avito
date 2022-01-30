from django.db import models
from django.contrib.auth.models import AbstractUser

from avito2_0 import settings


class User(AbstractUser):
    role = models.IntegerField('role', null=True)
    login = models.CharField('login', max_length=20)
    email = models.EmailField('email', max_length=40)
    pwd = models.CharField('pwd', max_length=20)
    phone = models.CharField('phone', max_length=11)
    name = models.CharField('name', max_length=60)
    city = models.CharField('city', null=True, blank=True, max_length=20)

    # ДОБАВИТЬ ПОЛЕ АВАТАРКИ

    def __str__(self):
        if User.is_staff:
            return self.username
        else:
            return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',  blank=True, null=True, on_delete=models.CASCADE)
    level = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='user', default='1')
    name = models.CharField('name', max_length=30)
    text = models.TextField('text', max_length=320)
    price = models.CharField('price', max_length=10)
    status = models.CharField('status', blank=True, null=True, max_length=15)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    address = models.TextField('address', max_length=320, null=True, blank=True,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Image(models.Model):
    image = models.FileField(upload_to='images', verbose_name='image')
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total_price = models.DecimalField(max_digits=9, decimal_places=2)


# class Cart(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='user', default=1)
#     cart_items = models.ManyToManyField(CartItem, blank=True)
#     cart_total_price = models.DecimalField(max_digits=9, decimal_places=0)
#
#     def __str__(self):
#         return str(self.id)
#
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзины'


# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE, verbose_name='user', default='1')
#
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     paid = models.BooleanField(default=False)
#
#     class Meta:
#         ordering = ('-created',)
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'
#
#     def __str__(self):
#         return 'Order {}'.format(self.id)
#
#     def get_total_cost(self):
#         return sum(item.get_cost() for item in self.items.all())
#
#
