from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
import django.contrib.auth
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from .models import *

import main_app.main_app.forms


@csrf_protect
def index(request):
    if request.method == 'POST':
        form = main_app.main_app.forms.LoginForm(request.POST)
        if form.is_valid():
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
    else:
        form = main_app.main_app.forms.LoginForm()
        return render(request, '../templates/main_app/index.html', {'form': form})


def member_bio(request):
    if request.user.is_authenticated:
        items = Item.objects.filter(user_id=request.user.id)
        images = Image.objects.all()

        template = loader.get_template('../templates/main_app/member_bio.html')

        return HttpResponse(template.render(locals()))
    else:
        return render(request, '../templates/main_app/member_bio.html')


@csrf_protect
def add_item(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = main_app.main_app.forms.AddItemForm(request.POST, request.FILES)
            if form.is_valid():
                name = request.POST.get('name')
                category = request.POST.get('category')
                text = request.POST.get('text')
                status = request.POST.get('status')
                item = Item.objects.create(
                    user_id=request.user.id,
                    name=name,
                    category=category,
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
def search(request):
    if request.method == 'POST':
        form = main_app.main_app.forms.SearchForm(request.POST)
        if form.is_valid():
            search_text = request.POST.get('search_text')
            category = request.POST.get('category')
            item_all = Item.objects.all()
            image_all = Image.objects.all()
            user_all = User.objects.all()
            template = loader.get_template('../templates/main_app/index.html')
            return render(request, template, locals())
        else:
            print(form.errors)
            return HttpResponse("Invalid form")
    else:
        form = main_app.main_app.forms.SearchForm()
        return render(request, '../templates/main_app/index.html', {'form': form})
