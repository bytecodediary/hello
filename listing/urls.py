from django.urls import path
from . import views

app_name = "property"

urlpatterns = [
    path('propertylist/', views.PropertyListCreateView.as_view(), name="propertylist"),
    path('property/<slug:slug>/', views.PropertyDetailView.as_view(), name='property-details'),
    path('notifications', views.NotificationListView.as_view(), name='notification'),
    path('notification/<int:pk>/', views.NotificationAPIView.as_view(), name='notification-detail'),
    path('notification/read', views.MarkAllAsReadView.as_view(), name='mark-as-read'),
    path('create/device/', views.CreateDeviceAPIView.as_view(), name='create-device'),
]