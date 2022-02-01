import re
from decimal import Decimal

from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate
import django.contrib.auth
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import *

import main_app.main_app.forms


@csrf_exempt
def index(request):
    if request.method == 'POST':
        cat_1 = Category.objects.filter(level=0)
        if request.POST.get('form_type') == 'login_form':
            login_form = main_app.main_app.forms.LoginForm(request.POST)
            if login_form.is_valid():
                login = request.POST.get('login', None)
                pwd = request.POST.get('pwd', None)
                user = authenticate(username=login, password=pwd)
                if user is not None:
                    if user.is_active:
                        django.contrib.auth.login(request, user)
                        return HttpResponseRedirect("/")
                    else:
                        return HttpResponse("disabled account")
                else:
                    return HttpResponse("user none")
            else:
                return HttpResponse("Invalid data form")

        if request.POST.get('form_type') == 'search_form':
            search_form = main_app.main_app.forms.SearchForm(request.POST)

            if search_form.is_valid():
                search_text = request.POST.get('search_text')
                category = request.POST.get('category')
                item_all = list()
                item_search = Item.objects.all()
                for i in item_search:
                    if (search_text.upper().lower() in i.name.upper().lower()) and (i.category_id == int(category)):
                        if i.category_id == int(category):
                            item_all.append(i)
                image_all = Image.objects.all()
                user_all = User.objects.all()
                template = loader.get_template('../templates/main_app/index.html')
                return HttpResponse(template.render(locals()))
            else:
                print(search_form.errors)
                return HttpResponse("Invalid form")
    else:
        image_all = Image.objects.all()
        item_all = Item.objects.all()
        login_form = main_app.main_app.forms.LoginForm()
        search_form = main_app.main_app.forms.SearchForm()

        cat_1 = Category.objects.filter(level=0)

        return render(request, '../templates/main_app/index.html',
                      {'login_form': login_form, 'search_form': search_form, 'item_all': item_all,
                       'image_all': image_all, 'cat_1': cat_1})


# @csrf_exempt
# def index(request):
#     # item_all = Item.objects.all()
#     # image_all = Image.objects.all()
#     # user_all = User.objects.all()
#     if request.method == 'POST':
#         if request.POST.get('form_type') == 'login_form':
#             login_form = main_app.main_app.forms.LoginForm(request.POST)
#             if login_form.is_valid():
#                 login = request.POST.get('login', None)
#                 pwd = request.POST.get('pwd', None)
#                 user = authenticate(username=login, password=pwd)
#                 if user is not None:
#                     if user.is_active:
#                         django.contrib.auth.login(request, user)
#                         return HttpResponseRedirect("/")
#                     else:
#                         return HttpResponse("disabled account")
#                 else:
#                     return HttpResponse("user none")
#             else:
#                 return HttpResponse("Invalid data form")
#
#         if request.POST.get('form_type') == 'search_form':
#             search_form = main_app.main_app.forms.SearchForm(request.POST)
#             if search_form.is_valid():
#                 search_text = request.POST.get('search_text')
#                 category = request.POST.get('category')
#                 item_all = Item.objects.filter(Q(category=category) and Q(name__icontains=search_text))
#                 image_all = Image.objects.all()
#                 user_all = User.objects.all()
#                 template = loader.get_template('../templates/main_app/index.html')
#                 return HttpResponse(template.render(locals()))
#             else:
#                 print(search_form.errors)
#                 return HttpResponse("Invalid form")
#     else:
#         image_all = Image.objects.all()
#         item_all = Item.objects.all()
#         login_form = main_app.main_app.forms.LoginForm()
#         search_form = main_app.main_app.forms.SearchForm()
#         return render(request, '../templates/main_app/index.html',
#                       {'login_form': login_form, 'search_form': search_form})
#
# @csrf_exempt
# def index(request):
#     if request.method == 'POST':
#         if request.POST.get('form_type') == 'login_form':
#             login_form = main_app.main_app.forms.LoginForm(request.POST)
#             if login_form.is_valid():
#                 login = request.POST.get('login', None)
#                 pwd = request.POST.get('pwd', None)
#                 user = authenticate(username=login, password=pwd)
#                 if user is not None:
#                     if user.is_active:
#                         django.contrib.auth.login(request, user)
#                         return HttpResponseRedirect("/")
#                     else:
#                         return HttpResponse("disabled account")
#                 else:
#                     return HttpResponse("user none")
#             else:
#                 return HttpResponse("Invalid data form")
#
#         if request.POST.get('form_type') == 'search_form':
#             search_form = main_app.main_app.forms.SearchForm(request.POST)
#
#             if search_form.is_valid():
#                 search_text = request.POST.get('search_text')
#                 category = request.POST.get('category')
#                 item_all = list()
#                 item_search = Item.objects.all()
#                 for i in item_search:
#                     if search_text.upper().lower() in i.name.upper().lower() or search_text.upper().lower() in i.text.upper().lower():
#                         item_all.append(i)
#
#                 # item_all = Item.objects.filter(category=category, name=search_text)
#                 image_all = Image.objects.all()
#                 user_all = User.objects.all()
#                 template = loader.get_template('../templates/main_app/index.html')
#                 return HttpResponse(template.render(locals()))
#             else:
#                 print(search_form.errors)
#                 return HttpResponse("Invalid form")
#     else:
#         image_all = Image.objects.all()
#         item_all = Item.objects.all()
#         login_form = main_app.main_app.forms.LoginForm()
#         search_form = main_app.main_app.forms.SearchForm()
#
#         return render(request, '../templates/main_app/index.html',
#                       {'login_form': login_form, 'search_form': search_form, 'item_all': item_all,
#                        'image_all': image_all})


def member_bio(request):
    if request.user.is_authenticated:
        items = Item.objects.filter(user_id=request.user.id)
        images = Image.objects.all()
        image_item = list()
        for i in items:
            for im in images:
                if im.item_id == i.id:
                    image_item.append(im)
                    break

        template = loader.get_template('../templates/main_app/bio.html')
        return HttpResponse(template.render(locals()))
    else:
        return render(request, '../templates/main_app/bio.html')


@csrf_protect
def add_item(request, id):
    if request.user.is_authenticated:
        cat_3 = Category.objects.filter(level=2, parent_id=id)
        if request.method == 'POST':
            form = main_app.main_app.forms.AddItemForm(request.POST, request.FILES)
            if form.is_valid():
                name = request.POST.get('name')
                price = request.POST.get('price')
                address = request.POST.get('address')
                category = request.POST.get('category')
                text = request.POST.get('text')
                # status = request.POST.get('status')
                status = 'yes'
                item = Item.objects.create(
                    user_id=request.user.id,
                    name=name,
                    price=price,
                    address=address,
                    category_id=category,
                    text=text,
                    status=status)
                for f in request.FILES.getlist('image'):
                    image = Image(item=item, image=f)
                    image.save()
                item.save()
                return HttpResponseRedirect('/bio')
            else:
                print(form.errors)
                return HttpResponse('not valid form')
        else:
            form = main_app.main_app.forms.AddItemForm()
            return render(request, '../templates/main_app/add_item.html', {'form': form, 'cat_3': cat_3})
    else:
        return HttpResponseRedirect('index')


@csrf_protect
def add_item_category(request):
    cat_1 = Category.objects.filter(level = 0)
    return render(request, '../templates/main_app/add_item_category.html', {'cat_1': cat_1})


@csrf_protect
def add_item_category_select(request, id):
    cat_1 = Category.objects.filter(level = 0)
    cat_2 = Category.objects.filter(level=1, parent_id=id)
    aa = Category.objects.filter(level=0, id=id)
    up_name = ''
    for a in aa:
        up_name =a.name
    return render(request, '../templates/main_app/add_item_category.html', {'cat_1': cat_1, 'cat_2': cat_2, 'up_name': up_name})


def del_item(request, id):
    if request.user.is_authenticated:
        Item.objects.filter(id=id).delete()
        return HttpResponseRedirect('/bio')
    else:
        return HttpResponseRedirect('/bio')


@csrf_protect
def registration(request):
    if request.method == "POST":
        form = main_app.main_app.forms.RegForm(request.POST)
        if form.is_valid():
            if request.POST.get("pwd") == request.POST.get("pwd2"):
                login = request.POST.get("login")
                password = request.POST.get("pwd")
                email = request.POST.get("email")
                name = request.POST.get('name')
                city = request.POST.get('city')
                role = request.POST.get('role')
                phone = request.POST.get('phone')
                user = User.objects.create_user(username=login,
                                                password=password,
                                                email=email,
                                                name=name,
                                                city=city,
                                                role=role,
                                                phone=phone)
                user.save()
                user = authenticate(username=login, password=password)
                if user is not None:
                    if user.is_active:
                        django.contrib.auth.login(request, user)
                        return HttpResponseRedirect("/")
                else:
                    return HttpResponse("user none")
            else:
                return HttpResponse("Invalid data pwd")
        else:
            print(form.errors)
            return HttpResponse("Invalid data form")
    else:
        form = main_app.main_app.forms.RegForm()
        return render(request, '../templates/main_app/registration.html', {'form': form})


@csrf_protect
def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect("/")


@csrf_protect
def redaction(request):
    user = User.objects.all()
    if request.method == "POST":
        form = main_app.main_app.forms.RedactForm(request.POST)
        for user in user:
            if user.id == request.user.id:
                if form.is_valid():
                    user.email = request.POST.get("email")
                    user.first_name = request.POST.get('name')
                    user.last_name = request.POST.get('surname')
                    user.city = request.POST.get('city')
                    user.phone = request.POST.get('phone')
                    user.save()
                else:
                    print(form.errors)
                    return HttpResponse("Invalid data form")
    else:
        form = main_app.main_app.forms.RedactForm()
        return render(request, '../templates/main_app/redaction.html', {'form': form})
    return HttpResponseRedirect('/bio')


def single(request, id):
    cart_items = list()
    cart_id = list()
    ids = Item.objects.values_list('id', flat=True)
    if 'cart' not in request.session:
        request.session['cart'] = list()
    for c in request.session['cart']:
        cart_items.append(Item.objects.get(id=c))
    for i in ids:
        for c in cart_items:
            if i == c.id:
                cart_id.append(i)
    single_item = Item.objects.filter(id=id)
    image_all = Image.objects.all()
    template = loader.get_template('../templates/main_app/single.html')
    return HttpResponse(template.render(locals()))


def cart(request):
    count = 0
    total = 0
    items = list()
    cart_items = list()
    if 'cart' not in request.session:
        request.session['cart'] = list()
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        for c in request.session['cart']:
            count = count + 1
            items.append(Item.objects.get(id=c))
            cartItem = CartItem.objects.create(item_total_price=Item.objects.get(id=c).price,
                                               item_id=Item.objects.get(id=c).id, )
            cartItem.save()
            cart_items.append(cartItem)
            # итоговая стоимость без учета количсетва
            price = cartItem.item_total_price
            total = Decimal(price) + total
    image_all = Image.objects.all()
    # cart_item = CartItem.objects.filter(id=id)
    template = loader.get_template('../templates/main_app/cart.html')
    return HttpResponse(template.render(locals()))


def add_to_cart(request, id):
    cart_items = list()
    if request.user.is_authenticated:
        if 'cart' not in request.session:
            request.session['cart'] = list()
        if id not in request.session['cart']:
            request.session['cart'].append(int(id))
        request.session.save()
        for c in request.session['cart']:
            for ci in cart_items:
                if c != ci.id:
                    cart_items.append(Item.objects.get(id=c))
    else:
        return HttpResponse('user not auth')
    return HttpResponse(cart(request))


def del_item_cart(request, id):
    cart_items = list()
    if request.user.is_authenticated:
        if id in request.session['cart']:
            request.session['cart'].remove(int(id))
        request.session.save()
        for c in request.session['cart']:
            cart_items.append(Item.objects.get(id=c))
    return HttpResponse(cart(request))


def make_order(request):
    request.session['cart'].clear()
    template = loader.get_template('../templates/main_app/index.html')
    return HttpResponse(template.render(locals()))


# @csrf_protect
# def cat(request):
#     if request.method == 'POST':
#         cat_1 = Category.objects.filter(level=0)
#         if request.POST.get('form_type') == 'login_form':
#             login_form = main_app.main_app.forms.LoginForm(request.POST)
#             if login_form.is_valid():
#                 login = request.POST.get('login', None)
#                 pwd = request.POST.get('pwd', None)
#                 user = authenticate(username=login, password=pwd)
#                 if user is not None:
#                     if user.is_active:
#                         django.contrib.auth.login(request, user)
#                         return HttpResponseRedirect("/")
#                     else:
#                         return HttpResponse("disabled account")
#                 else:
#                     return HttpResponse("user none")
#             else:
#                 return HttpResponse("Invalid data form")
#
#         if request.POST.get('form_type') == 'search_form':
#             search_form = main_app.main_app.forms.SearchForm(request.POST)
#
#             if search_form.is_valid():
#                 search_text = request.POST.get('search_text')
#                 category = request.POST.get('category')
#                 item_all = list()
#                 item_search = Item.objects.all()
#                 for i in item_search:
#                     # if search_text.upper().lower() in i.name.upper().lower() or search_text.upper().lower() in i.text.upper().lower():
#                     if search_text.upper().lower() in i.name.upper().lower():
#                         item_all.append(i)
#
#                 image_all = Image.objects.all()
#                 user_all = User.objects.all()
#                 template = loader.get_template('../templates/main_app/cat.html')
#                 return HttpResponse(template.render(locals()))
#             else:
#                 print(search_form.errors)
#                 return HttpResponse("Invalid form")
#     else:
#         image_all = Image.objects.all()
#         item_all = Item.objects.all()
#         login_form = main_app.main_app.forms.LoginForm()
#         search_form = main_app.main_app.forms.SearchForm()
#
#         cat_1 = Category.objects.filter(level=0)
#
#         return render(request, '../templates/main_app/cat.html',
#                       {'login_form': login_form, 'search_form': search_form, 'item_all': item_all,
#                        'image_all': image_all, 'cat_1': cat_1})


def child_cat(parent_cat, child_level):
    child_cat = Category.objects.filter(level=child_level)
    child_categories = list()
    for parent_c in parent_cat:
        for child_c in child_cat:
            if child_c.parent_id == parent_c.id:
                child_categories.append(child_c)
    return child_categories


@csrf_protect
def show_categories_2(request, id):  # id первой категории
    category = Category.objects.filter(level=0, id=id)
    up_cat = category[0].name
    child = child_cat(category, 1)
    item_all = cat_items(category)
    image_all = Image.objects.all()
    return render(request, '../templates/main_app/index.html',
                  {'item_all': item_all, 'image_all': image_all, 'cat_2': child, 'main_cat': up_cat})


@csrf_protect
def show_categories_3(request, id):  # id второй категории
    category = Category.objects.filter(level=1, id=id)
    up_cat = category[0].name
    up_cat_parent = category[0].parent_id
    cat = Category.objects.filter(level=0, id=up_cat_parent)
    up_cat2 = Category.objects.filter(level=0, id=up_cat_parent)
    child = child_cat(category, 2)
    if not child:
        return HttpResponse(show_categories_2(request, id=up_cat_parent))
    item_all = cat_items(category)
    image_all = Image.objects.all()
    return render(request, '../templates/main_app/index.html',
                  {'item_all': item_all, 'image_all': image_all, 'cat_3': child, 'main_cat1': up_cat2,
                   'main_cat2': up_cat})


def cat_items(category):
    cat_3 = Category.objects.filter(level=2)
    item_all = list()
    items = Item.objects.all()
    lev = 0
    for a in category:
        lev = a.level + 1
    child = child_cat(category, lev)
    for c in child:
        if c.level == 2:
            for it in items:
                if it.category_id == c.id:
                    item_all.append(it)
        else:
            for cat3 in cat_3:
                if cat3.parent_id == c.id:
                    for it in items:
                        if it.category_id == cat3.id:
                            item_all.append(it)
    return item_all


def chose_cat(request, id):
    item_all = list()
    items = Item.objects.all()
    cat3 = Category.objects.filter(level=2, id=id)
    cat2 = Category.objects.filter(level=1, id=cat3[0].parent_id)
    cat1 = Category.objects.filter(level=0, id=cat2[0].parent_id)
    for it in items:
        if it.category_id == id:
            item_all.append(it)
    image_all = Image.objects.all()
    main_cat1 = cat1
    main_cat2 = cat2
    main_cat3 = cat3
    return render(request, '../templates/main_app/index.html',
                  {'item_all': item_all, 'image_all': image_all, 'main_cat1': main_cat1, 'main_cat2': main_cat2,
                   'main_cat3': main_cat3})
