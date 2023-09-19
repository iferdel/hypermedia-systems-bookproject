# contacts/forms.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewContactForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
