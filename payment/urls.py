from django.urls import path
from . import views

urlpatterns = [
    path('intents/', views.PaymentIntentView.as_view(), name='payment-intents'),
    path('callback/mpesa/<uuid:token>/', views.mpesa_callback, name='mpesa-callback'),
    path('', views.PaymentView.as_view(), name='payment'),
    path('transactions/', views.TransactionView.as_view(), name='transaction'),
    path('payment', views.PaymentView.as_view(), name='legacy-payment'),
    path('transactions', views.TransactionView.as_view(), name='legacy-transactions'),
]
