from django.shortcuts import render


def home(request):
    return render(request, "<H1>Ephemeris</H2>")
