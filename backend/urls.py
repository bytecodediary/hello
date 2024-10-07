from django.urls import path
from .views import UserRegistrationView, UserLoginView, PropertyListCreateView, PropertyDetailView, CartDeleteItemView, CartAddItemView,CartDetailView, CartUpdateItemView

app_name = "backend"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="api-register"),
    path("login/", UserLoginView.as_view(), name="api-login"),
    path('propertylist/', PropertyListCreateView.as_view(), name="property_list"),
    path('property/<slug:slug>/', PropertyDetailView.as_view(), name='property_details'),
    path('cart/', CartDetailView.as_view(), name='cart'),
    path('cart/add/', CartAddItemView.as_view(), name='cart-add'),
    path('cart/update/', CartUpdateItemView.as_view(), name='cart-update'),
    path('cart/<slug:slug>/delete/', CartDeleteItemView.as_view(), name='cart-delete')
]