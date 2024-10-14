from django.urls import path
from .views import OrderDetailView, OrderView, CancelOrderView, CheckoutView, OrderItemListView, OrderItemDetailView, CartAddItemView, CartDeleteItemView, CartDetailView, CartUpdateItemView

urlpatterns = [
    path('order', OrderView.as_view(), name='order'),
    path('order/<slug:slug>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/cancel/', CancelOrderView.as_view(), name='cancel-order'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('order/<slug:slug>/items/', OrderItemListView.as_view(), name='order-items-view'),
    path('order/<slug:slug>/items/<int:id>/', OrderItemDetailView.as_view(), name='order-item-details'),
    path('cart/', CartDetailView.as_view(), name='cart'),
    path('cart/add/', CartAddItemView.as_view(), name='cart-add'),
    path('cart/update/', CartUpdateItemView.as_view(), name='cart-update'),
    path('cart/<slug:slug>/delete/', CartDeleteItemView.as_view(), name='cart-delete'),
]