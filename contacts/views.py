# contacts/views.py
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    return render(request, "home.html")


def contacts(request):
    search = request.GET.get("q")
    if search is not None:
        users = User.objects.filter(username__icontains=search)
    else:
        users = User.objects.all()

    return render(request, "index.html", {"users": users})


def contacts_new(request):
    if request.method == 'POST':
        new_user = User(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            username=request.POST['username'],
            email=request.POST['email'],
        )
        new_user.save()

        return redirect("/contacts")

    else:
        new_user = User()
        return render(request, "new.html", {"contact": new_user})


def contacts_view(request, user_id=0):
    user = get_object_or_404(User, id=user_id)
    return render(request, "show.html", {"user": user})


def contacts_edit(request, user_id=0):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        return redirect("/contacts/" + str(user_id))

    elif request.method == 'DELETE':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        response = HttpResponse(status=303)
        response['Location'] = '/contacts'
        return response

    else:
        return render(request, "edit.html", {"user": user})
