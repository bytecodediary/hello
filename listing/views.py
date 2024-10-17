from .serializers import PropertySerializer
from .serializers import NotificationMiniSerializer, FCMDeviceSerializer
from rest_framework import status, generics, permissions
from .models import Property, Notification
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from rest_framework.exceptions import PermissionDenied, NotAcceptable
from fcm_django.models import FCMDevice
from django.utils.translation import gettext_lazy as _


#property views
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = (DjangoFilterBackend)
    filterset_class = PropertyFilter

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

# notification views

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationMiniSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(
            user=user,
            notification = Notification.is_read
        ).order_by('-received_at')
        return queryset

class NotificationAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_classes = NotificationMiniSerializer
    queryset = Notification.objects.all()

    def retrieve(self,request, *args, **kwargs):
        notification = self.get_object(user=request.user)
        if notification.user != request.user:
            raise PermissionDenied(
                'This notification does not belong to you'
            )
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        notification = self.get_object(user = request.user)
        if notification.user != request.user:
            raise PermissionDenied(
                'Action not allowed as this notification does not belong to you'
            )
        notification.delete()
        return Response({'details': _('The notification has been deleted successfully')}, status=status.HTTP_204_NOT_FOUND)

class MarkAllAsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = self.request.user
        notifications = Notification.objects.filter(
            user=user, status = Notification.is_read is False
        )

        for notification in notifications:
            if notification.user != request.user:
                raise PermissionDenied(
                    'Action not allowed'
                )
            notification.status = notification.is_read is True

            notification.save()
        return Response('No new notification', status=status.HTTP_200_OK)

class CreateDeviceAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user
        registration_id = request.data.get("registration_id", None)
        type = request.data.get("type", None)
        device = FCMDevice.objects.filter(registration_id=registration_id, type=type)
        if device.count() > 0:
            raise NotAcceptable("This Device already exists.")
        serializer = FCMDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
