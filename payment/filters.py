import django_filters
from .models import Payment

class PaymentFilters(django_filters.FilterSet):
  transaction_type = django_filters.CharFilter(lookup_expr='icontains')

  class Meta:
    model = Payment
    fields = ['transaction_type']