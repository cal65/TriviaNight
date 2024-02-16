from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    """
    return templates/landing.html
    """
    t = "landing.html"
    return render(request, t)
