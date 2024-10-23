from rest_framework import generics, permissions, status
from .models import Client, Agent, Owner, CustomUser
from .serializers import AgentSerializer, ClientSerializer, OwnerSerializer, ChangeUserTypeSerializer, CustomUserSerializer, LoginSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view

#custom user views
class ChangeUserTypeView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangeUserTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return validation errors instead of data on failure
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # print("Received request data:", request.data) 
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                'message': 'login successful',
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_200_OK)
        # print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#profiles
class AgentProfileView(generics.GenericAPIView):
    queryset = Agent.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AgentSerializer

    def get_objects(self):
        return self.request.user.agent

class ClientProfileView(generics.GenericAPIView):
    queryset = Client.objects.all()
    permission_classes =[permissions.IsAuthenticated]
    serializer_class = ClientSerializer

    def get_objects(self):
        return self.request.user.customer
    
class OwnerProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def get_objects(self):
        return self.request.user.owner


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})

@api_view(['GET'])
def check_authentification(request):
    if request.user.is_authenticated:
        return Response({"authenticated":True, "username": request.user.username})
    return Response({"authenticated": False})