"""main_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from avito2_0 import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('bio', views.member_bio, name='mem_bio'),
    path('add_item/<int:id>', views.add_item, name='add_item'),
    path('add_item_category', views.add_item_category, name='add_item_category'),
    path('add_item_category/<int:id>', views.add_item_category_select, name='add_item_category_select'),
    path('registration', views.registration, name='reg'),
    path('redaction', views.redaction, name='redaction'),
    path('logout', views.logout, name='logout'),
    path(r'^single/(?P<id>\w+)$', views.single, name='single'),
    path(r'cart', views.cart, name='cart'),
    path(r'bio/(?P<int:id>\d+)$', views.del_item, name='del_item'),
    path(r'^add_to_cart/(?P<int:id>\d+)$', views.add_to_cart, name='add_to_cart'),
    path(r'^del_item_cart/(?P<int:id>\d+)$', views.del_item_cart, name='del_item_cart'),
    path(r'make_order', views.make_order, name='make_order'),

    # path('cat', views.index, name='cat'),
    # path(r'^show_categories/(?P<int:id>\d+)$', views.show_categories, name='show_categories'),
    path('categories/<int:id>', views.show_categories_2, name='show_second_cat'),
    path('categories/all/<int:id>', views.show_categories_3, name='show_third_cat'),
    path('categorie/<int:id>', views.chose_cat, name='chose_cat'),

]
if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
