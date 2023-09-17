# contacts/views.py

from django.urls import path
from . import views

urlpatterns = [
    path("contacts/", views.contacts, name="contacts"),
    path("contacts/new/", views.contacts_new, name="contacts_new"),
]
