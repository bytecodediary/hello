from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import CustomUser,Payment,Property,CartItem,Cart,Property_Features, Order, OrderItem, Agent, Client, Property_Lord,  Image, Transaction, Notification

from CustomUser.Serializer import cusomSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = customSerializer
    permission_classes = [AllowAny]