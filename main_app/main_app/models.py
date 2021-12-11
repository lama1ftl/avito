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
    city = models.CharField('city', max_length=20)

    # ДОБАВИТЬ ПОЛЕ АВАТАРКИ

    def __str__(self):
        if User.is_staff:
            return self.username
        else:
            return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='user', default='1')

    name = models.CharField('name', max_length=30)
    text = models.TextField('text', max_length=320)
    price = models.CharField('price', max_length=10)
    status = models.CharField('status', max_length=15)
    category = models.CharField('category', max_length=30, default='cat1')

    # В БУДУЩЕМ:
    #     КОММЕНТЫ К ТОВАРАМ

    # ДОБАВИТЬ ЛИСТ ФОТОК
    # ДОБАВИТЬ ВСЯКИЕ ДАТЫ

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
    item_total_price = models.DecimalField(max_digits=9, decimal_places=0)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='user', default=1)
    cart_items = models.ManyToManyField(CartItem, blank=True)
    cart_total_price = models.DecimalField(max_digits=9, decimal_places=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
