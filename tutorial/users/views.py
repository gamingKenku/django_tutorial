from django.shortcuts import render
from .forms import RegisterForm, LoginForm, UserInfoChange
from django.contrib.auth import login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from hello.models import Book
from .models import OrderHistory
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from typing import NamedTuple


class OrderRecord (NamedTuple):
    order_date: str
    book_list: list
    price: float


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(request)
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            print(register_form.errors)

    register_form = RegisterForm()
    return render(request, "users/register.html", context={'register_form': register_form})


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")

        messages.error(request, "Неправильный логин или пароль.")

    login_form = LoginForm(request)
    return render(request, "users/login.html", context={"login_form": login_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "users/profile.html")
    else:
        return HttpResponseRedirect("/")


def redact(request):
    if request.method == "POST":
        user_change_form = UserInfoChange(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return HttpResponseRedirect('/users/profile')
        else:
            print(user_change_form.errors)

    user_change_form = UserInfoChange(instance=request.user)
    return render(request, "users/redact.html", context={"user_change_form": user_change_form})


def change_password(request):
    if request.method == "POST":
        change_password_form = PasswordChangeForm(request.user, request.POST)
        if change_password_form.is_valid():
            user = change_password_form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect('/users/profile/')
        else:
            print(change_password_form.errors)

    change_password_form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', context={'change_password_form': change_password_form})


def add_to_cart(request, book_id):
    try:
        Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Книги не существует.")

    saved_list = request.session['cart']
    saved_list.append(book_id)
    request.session['cart'] = saved_list
    return HttpResponseRedirect("/")


def cart(request):
    saved_list = request.session['cart']
    books = []
    sum_price = 0

    for book_id in saved_list:
        book = Book.objects.get(id=book_id)
        books.append(book)
        sum_price += book.price

    return render(request, "users/cart.html", context={'books': books, 'sum_price': sum_price})


def order(request):
    saved_list = request.session['cart']
    now = datetime.now()
    user = request.user

    try:
        for book_id in saved_list:
            Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('Книга не найдена.')

    for book_id in saved_list:
        OrderHistory.objects.create(
            user_id=user.id,
            book_id=book_id,
            order_date=now
        )

    saved_list = []
    request.session['cart'] = saved_list

    return HttpResponseRedirect('/')


def order_history(request):
    history = OrderHistory.objects\
        .filter(user_id=request.user.id)\
        .order_by('-order_date')
    order_list = []

    while history.count() != 0:
        max_date = history.first().order_date
        order_by_date = history.filter(order_date=max_date)
        book_list = list(order_by_date.values_list('book__title', flat=True))
        price = sum(list(order_by_date.values_list('book__price', flat=True)))

        order_list.append(OrderRecord(max_date, book_list, price))

        history = history.exclude(order_date=max_date)

    return render(request, 'users/order_history.html', context={"order_list": order_list})
