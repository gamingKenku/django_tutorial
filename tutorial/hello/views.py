from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Book
from django.core.paginator import Paginator


def home(request):
    books = Book.objects.all()

    paginator = Paginator(books, per_page=5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if 'cart' not in request.session.keys():
        request.session['cart'] = []

    return render(request, "home.html",
                  context={"page_obj": page_obj,
                           "page": page_number,
                           "cart_len": len(request.session['cart'])})


def redact(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Книги не существует.")

    if request.method == "GET":
        return render(request, "redact.html", {"book": book})
    elif request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.price = request.POST.get("price")
        book.release_date = request.POST.get("date")
        book.save()
        return HttpResponseRedirect("/")


def add(request):
    if request.method == "GET":
        return render(request, "add.html")
    elif request.method == "POST":
        Book.objects.create(title=request.POST.get("title"),
                            author=request.POST.get("author"),
                            price=request.POST.get("price"),
                            release_date=request.POST.get("release_date"))
        return HttpResponseRedirect("/")


def delete(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Книги не существует.")

    book.delete()
    return HttpResponseRedirect("/")


