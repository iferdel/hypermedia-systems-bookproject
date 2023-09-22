# contacts/urls.py

from django.urls import path
from .views import views, htmx_views

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("contacts/new/", views.contacts_new, name="contacts_new"),
    path("contacts/<int:user_id>/", views.contacts_view, name="contacts_view"),
    path("contacts/<int:user_id>/edit/", views.contacts_edit, name="contacts_edit"),
    path("contacts/bulk_delete/", views.contacts_bulk_delete, name="contacts_bulk_delete")
]

htmx_views = [
    path("check_username/", htmx_views.check_username, name="check-username"),
    path("check_email/", htmx_views.check_email, name="check-email"),
    path("contacts/count/", htmx_views.contacts_count, name="contacts-count"),
]

urlpatterns += htmx_views
