from django.urls import path
from .views import UserRegistrationView, UserLoginView, PropertyListCreateView, PropertyDetailView

app_name = "backend"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="api-register"),
    path("login/", UserLoginView.as_view(), name="api-login"),
    path('propertylist/', PropertyListCreateView.as_view(), name="property_list"),
    path('property/<slug:slug>/', PropertyDetailView.as_view(), name='property_details')
]