from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from core.models import Product


def products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, "core/products.html", context={"products": products})
