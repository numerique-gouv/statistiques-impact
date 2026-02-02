from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from core.models import Product


def last_indicators(request: HttpRequest) -> HttpResponse:
    last_indicators = sorted(
        [
            {
                "product": product,
                "last_indicators": product.last_indicators,
            }
            for product in Product.objects.all()
            if product.last_indicators
        ],
        key=lambda x: x["last_indicators"][0].date,
        reverse=True,
    )
    return render(
        request,
        "core/last_indicators.html",
        context={"last_indicators": last_indicators},
    )


def product(request, product_slug) -> HttpResponse:
    """Page for a single product"""

    product = get_object_or_404(Product, slug=product_slug)
    return render(request, "core/product.html", context={"product": product})
