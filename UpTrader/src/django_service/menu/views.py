from django.shortcuts import render


# Create your views here.
def menu(request, path):
    return render(request, "index.html")
