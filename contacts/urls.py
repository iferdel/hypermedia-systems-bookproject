# contacts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("contacts/new/", views.contacts_new, name="contacts_new"),
    path("contacts/<int:user_id>/", views.contacts_view, name="contacts_view"),
    path("contacts/<int:user_id>/edit/", views.contacts_edit, name="contacts_edit"),
    path("contacts/<int:user_id>/email/", views.contacts_email_get, name="contacts_email_get"),
]

htmx_views = [
    path("check_username/", views.check_username, name="check-username"),
]

urlpatterns += htmx_views
