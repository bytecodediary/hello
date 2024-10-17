from django.urls import path
from . import views

urlpatterns = [
    path('order', views.OrderView.as_view(), name='order'),
    path('order/<slug:slug>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('order/cancel/', views.CancelOrderView.as_view(), name='cancel-order'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('order/<slug:slug>/items/', views.OrderItemListView.as_view(), name='order-items-view'),
    path('order/<slug:slug>/items/<int:id>/', views.OrderItemDetailView.as_view(), name='order-item-details'),
    path('cart/', views.CartDetailView.as_view(), name='cart'),
    path('cart/add/', views.CartAddItemView.as_view(), name='cart-add'),
    path('cart/update/', views.CartUpdateItemView.as_view(), name='cart-update'),
    path('cart/<slug:slug>/delete/', views.CartDeleteItemView.as_view(), name='cart-delete'),
]