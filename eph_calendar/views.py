from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("<H1>Ephemeris</H2>")
