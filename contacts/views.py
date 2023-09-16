# contacts/views.py

from django.contrib.auth.models import User
from django.shortcuts import render


def contacts(request):
    search = request.GET.get("q")
    if search is not None:
        users = User.objects.filter(username__icontains=search)
    else:
        users = User.objects.all()

    return render(request, "index.html", {"users": users})
