from django.shortcuts import render
from .models import Property
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django import messages
from .serializers import CustomUserSerializer, ChangeUserTypeSerializer,LoginSerializer,PropertySerializer
from rest_framework import status, generics, permissions
from .models import CustomUser, Property
from rest_framework.response import Response

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


class ChangeUserTypeView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangeUserTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class =CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericApiView):
    serializer_class = LoginSerializer

    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            return Response({
                'message': 'login successful',
                user: {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            },  status=status.HTTP_201_CREATED,)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer