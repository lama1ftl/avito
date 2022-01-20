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
                    # if search_text.upper().lower() in i.name.upper().lower() or search_text.upper().lower() in i.text.upper().lower():
                    if search_text.upper().lower() in i.name.upper().lower():
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
def add_item(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # if request.POST.get('form_type') == 'add_item_form':
            form = main_app.main_app.forms.AddItemForm(request.POST, request.FILES)
            if form.is_valid():
                name = request.POST.get('name')
                price = request.POST.get('price')
                category = request.POST.get('category')
                text = request.POST.get('text')
                status = request.POST.get('status')
                item = Item.objects.create(
                    user_id=request.user.id,
                    name=name,
                    price=price,
                    category_id=category,
                    text=text,
                    status=status)
                for f in request.FILES.getlist('image'):
                    image = Image(item=item, image=f)
                    image.save()
                item.save()
                return HttpResponseRedirect('bio')
            else:
                print(form.errors)
                return HttpResponse('not valid form')
        else:
            form = main_app.main_app.forms.AddItemForm()
            return render(request, '../templates/main_app/add_item.html', {'form': form})
    else:
        return HttpResponseRedirect('index')


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
        # k = items.__len__()
        # print(items)
        # for i in items:
        #     for ci in cart_items:
        #         print(ci)
        #         if i != ci.item:
        #             cartItem = CartItem.objects.create(item = i)
        #             cart_items.append(cartItem)
        # cart_items.clear()
        # for p in cart_items:
        #     print(p)
        # print(items)
        # print(cart_items)
    # else:
    #     return HttpResponseRedirect("/")
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


@csrf_protect
def show_cat(request, id):
    cat1 = Category.objects.filter(level=0)
    cat_1 = list()
    cat2 = Category.objects.filter(level=1)
    cat_2 = list()
    cat_3 = Category.objects.filter(level=2)
    cat3 = Category.objects.filter(level=2, id=id)
    item_all = list()
    items = Item.objects.all()
    category = Category.objects.filter(level=2, id=id)
    category2 = list()

    for cat3 in cat3:
        for it in items:
            if cat3.id == it.category_id:
                item_all.append(it)

    for cat1 in cat1:
        for c2 in cat2:
            for cat3 in cat_3:
                if cat3.id == id:
                    if cat3.parent_id == c2.id:
                        if c2.parent_id == cat1.id:
                            cat_1.append(cat1)

    for c in cat2:
        for c3 in cat_3:
            if c3.id == id:
                if c3.parent_id == c.id:
                    category2.append(c)
                    break

    for cat3 in cat_3:
        if cat3.id == id:
            for cat in cat2:
                if cat3.parent_id == cat.id:
                    cat_2.append(cat)

    image_all = Image.objects.all()

    return render(request, '../templates/main_app/index.html',
                  {'item_all': item_all, 'image_all': image_all, 'cat_2': cat_2,
                   'cat_3': cat_3, 'category': category, 'category2': category2, 'cat_1': cat_1})


@csrf_protect
def show_categories(request, id):
    cat_1 = Category.objects.filter(level=0, id=id)
    cat2 = Category.objects.filter(level=1)
    cat_3 = Category.objects.filter(level=2)
    cat_2 = list()
    item_all = list()
    items = Item.objects.all()

    for cat2 in cat2:
        if cat2.parent_id == id:
            cat_2.append(cat2)

    for cat2 in cat_2:
        for cat3 in cat_3:
            if cat3.parent_id == cat2.id:
                for it in items:
                    if cat3.id == it.category_id:
                        item_all.append(it)

    image_all = Image.objects.all()
    return render(request, '../templates/main_app/index.html',
                  {'item_all': item_all, 'image_all': image_all, 'cat_2': cat_2, 'cat_3': cat_3})
