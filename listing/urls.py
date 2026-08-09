from django.urls import path
from . import views

app_name = "property"

urlpatterns = [
    path('propertylist/', views.PropertyListCreateView.as_view(), name="propertylist"),
    path('property/<slug:slug>/', views.PropertyDetailView.as_view(), name='property-details'),
    path('api/v1/listings/', views.PropertyListCreateView.as_view(), name='api-listings'),
    path('api/v1/provider/listings/', views.ProviderPropertyListCreateView.as_view(), name='api-provider-listings'),
    path('api/v1/listings/<slug:slug>/', views.PropertyDetailView.as_view(), name='api-listing-detail'),
    path('api/v1/listings/<slug:slug>/moderate/', views.PropertyModerationView.as_view(), name='api-listing-moderate'),
    path('api/v1/listings/<slug:slug>/favorite/', views.FavoriteToggleView.as_view(), name='api-listing-favorite'),
    path('api/v1/favorites/', views.FavoriteListView.as_view(), name='api-favorites'),
    path('api/v1/listings/<slug:slug>/inquiries/', views.InquiryCreateView.as_view(), name='api-listing-inquiry'),
    path('api/v1/account/inquiries/', views.SeekerInquiryListView.as_view(), name='api-account-inquiries'),
    path('api/v1/provider/inquiries/', views.ProviderInquiryListView.as_view(), name='api-provider-inquiries'),
    path('api/v1/provider/inquiries/<int:pk>/', views.ProviderInquiryUpdateView.as_view(), name='api-provider-inquiry-update'),
    path('api/v1/notifications/', views.NotificationListView.as_view(), name='api-notifications'),
    path('api/v1/notifications/read/', views.MarkAllAsReadView.as_view(), name='api-notifications-read'),
    path('notifications', views.NotificationListView.as_view(), name='notification'),
    path('notification/<int:pk>/', views.NotificationAPIView.as_view(), name='notification-detail'),
    path('notification/read', views.MarkAllAsReadView.as_view(), name='mark-as-read'),
    path('create/device/', views.CreateDeviceAPIView.as_view(), name='create-device'),
]
