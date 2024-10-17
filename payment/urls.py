from django.urls import path
from . import views

urlpatterns = [
    path('payment', views.PaymentView.as_view(), name='payment'),
    path('transactions', views.TransactionView.as_view(), name='transaction'),
]