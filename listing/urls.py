from django.urls import path
from .views import PropertyListCreateView, PropertyDetailView
from .views import NotificationListView, NotificationAPIView, MarkAllAsReadView, CreateDeviceAPIView

app_name = "property"

urlpatterns = [
    path('propertylist/', PropertyListCreateView.as_view(), name="propertylist"),
    path('property/<slug:slug>/', PropertyDetailView.as_view(), name='property-details'),
    path('notifications', NotificationListView.as_view(), name='notification'),
    path('notification/<int:pk>/', NotificationAPIView.as_view(), name='notification-detail'),
    path('notification/read', MarkAllAsReadView.as_view(), name='mark-as-read'),
    path('create/device/', CreateDeviceAPIView.as_view(), name='create-device'),
]