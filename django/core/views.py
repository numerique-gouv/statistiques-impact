from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from core.models import Product


def index(request):
    return render(request, "core/index.html")


def products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, "core/products.html", context={"products": products})


def accessibility(request: HttpRequest) -> HttpResponse:
    return render(request, "core/accessibility.html")
