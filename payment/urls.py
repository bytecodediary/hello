from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentView.as_view(), name='payment'),
    path('transactions/', views.TransactionView.as_view(), name='transaction'),
    path('payment', views.PaymentView.as_view(), name='legacy-payment'),
    path('transactions', views.TransactionView.as_view(), name='legacy-transactions'),
]
