from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def index(request):
    return render(request, "core/index.html")


def accessibility(request: HttpRequest) -> HttpResponse:
    return render(request, "core/accessibility.html")
