from django.contrib.auth.models import User
from django.http import HttpResponse


def check_username(request):
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
        return HttpResponse("<div id='email-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='email-error' class='success'>This username is available</div>")


def check_email(request):
    email = request.POST.get('email')
    if User.objects.filter(email=email).exists():
        return HttpResponse("<div id='email-error' class='error'>This email already exists</div>")
    else:
        return HttpResponse("<div id='email-error' class='success'>This email is available</div>")


def contacts_count(request):
    count = User.objects.all().count()
    return HttpResponse("(" + str(count) + " total Contacts)")
