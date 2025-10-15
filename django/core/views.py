from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from core.models import Product


def products(request: HttpRequest) -> HttpResponse:
    products_last_indicators = sorted(
        [
            {
                "name": product.nom_service_public_numerique,
                "last_indicators": product.last_indicators,
            }
            for product in Product.objects.all()
            if product.last_indicators
        ],
        key=lambda x: x["last_indicators"][0].date,
        reverse=True,
    )
    return render(
        request, "core/products.html", context={"products": products_last_indicators}
    )
