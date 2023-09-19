# contacts/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    return render(request, "home.html")


def contacts(request):
    search = request.GET.get("q")
    if search is not None:
        users_list = User.objects.filter(username__icontains=search)
    else:
        users_list = User.objects.all()

    paginator = Paginator(users_list, 10)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.headers.get("HX-Request"):
        return render(request, "partial_users.html", {"users": users})

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
        return render(request, "new.html")


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


def contacts_email_get(request, user_id=0):
    user = get_object_or_404(User, id=user_id)
    user.email = request.GET.get('email')

    validator = EmailValidator()
    errors = {}
    try:
        validator(user.email)
    except ValidationError as e:
        errors['email'] = e.message

    return HttpResponse(errors.get('email', ''))
