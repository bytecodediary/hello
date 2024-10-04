from django.shortcuts import render
from .models import Property
from django.contrib.auth.forms import UserCreationForm, user
from django.contrib.auth import login
from django.contrib.auth.models import User
from django import messages
from .serializers import CustomUserSerializer, GroupSerializer

# Create your views here.
def property_view(request):
    properties = Property.objects.all()
    context = {"properties":properties}
    return render(request, "backend/index.html", context)

def register_view(request):
    if request.method =="POST":
        form  = UserCreationForm(request.Post)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if User.objects.filter(username=username).exists():
                pass


# def 