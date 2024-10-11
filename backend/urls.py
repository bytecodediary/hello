from django.urls import path
from .views import UserRegistrationView, UserLoginView, PropertyListCreateView, PropertyDetailView, CartDeleteItemView, CartAddItemView,CartDetailView, CartUpdateItemView
from .views import OwnerProfileView, AgentProfileView, ClientProfileView

app_name = "backend"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('propertylist/', PropertyListCreateView.as_view(), name="propertylist"),
    path('property/<slug:slug>/', PropertyDetailView.as_view(), name='property_details'),
    path('cart/', CartDetailView.as_view(), name='cart'),
    path('cart/add/', CartAddItemView.as_view(), name='cart-add'),
    path('cart/update/', CartUpdateItemView.as_view(), name='cart-update'),
    path('cart/<slug:slug>/delete/', CartDeleteItemView.as_view(), name='cart-delete'),
    path('profile/client', ClientProfileView.as_view(), name='client_profile'),
    path('profile/agent', AgentProfileView.as_view(), name='agent_profile'),
    path('profile/owner', OwnerProfileView.as_view(), name='owner-profile'),
]