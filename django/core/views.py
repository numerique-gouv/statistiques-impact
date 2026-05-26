from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from core.models import Product


def last_records(request: HttpRequest) -> HttpResponse:
    last_records = sorted(
        [
            {
                "product": product,
                "last_records": product.last_records,
            }
            for product in Product.objects.all()
            if product.last_records
        ],
        key=lambda x: x["last_records"][0].date,
        reverse=True,
    )
    return render(
        request,
        "core/last_records.html",
        context={"last_records": last_records},
    )


def product(request: HttpRequest, product_slug) -> HttpResponse:
    """Page for a single product"""

    product = get_object_or_404(Product, slug=product_slug)
    return render(request, "core/products_details.html", context={"product": product})
