# contacts/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


import urllib.parse

from contacts.forms import NewContactForm


def home(request):
    return render(request, "home.html")


def contacts(request):
    search = request.GET.get("q")
    if search is not None:
        users_list = User.objects.filter(username__icontains=search)
        if request.headers.get("HX-Trigger") == "search":
            return render(request, "rows.html", {"users": users_list})
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

    return render(request, "index.html", {"users": users})


def contacts_new(request):
    if request.method == 'POST':
        form = NewContactForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_unusable_password()
            new_user.save()
            return redirect("/contacts")
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = NewContactForm()

    return render(request, "new.html", {'form': form})


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
        # Differentiate between delete requests that belong to the same view
        # the delete-btn belongs to the edit page as it is, the else belongs
        # to the delete request available in the anchor tag.
        if request.headers.get('HX-Trigger') == 'delete-btn':
            response = HttpResponse(status=303)
            response['Location'] = '/contacts'
            return response
        else:
            return HttpResponse("")
    else:
        return render(request, "edit.html", {"user": user})


def contacts_bulk_delete(request):

    if request.method == 'DELETE':
        body = request.body.decode('utf-7')
        data = urllib.parse.parse_qs(body)
        selected_users_ids = list(map(int, data.get("selected_contact_ids", [])))

        for user_id in selected_users_ids:
            user = get_object_or_404(User, id=user_id)
            user.delete()

        users_list = User.objects.all()

        paginator = Paginator(users_list, 11)
        page = request.GET.get('page')

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(2)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request, "index.html", {"users": users})
