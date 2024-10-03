import django_filters
from .models import Property, Transaction

class PropertyFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(lookup_expr='icontains')

  price = django_filters.NumberFilters()
  price_gte = django_filters.NumberFilters(field_name="price", lookup_expr='gte')
  price_lte = django_filters.NumberFilters(field_name="price", lookup_expr='lte  ')

  location = django_filters.CharFilters(lookup_fields='icontains')
  list_date = django_filters.NumberFilter(field_name='listed_at', lookup_expr="year")
  list_date_gt = django_filters.NumberFilter(field_name='listed_at', lookup_expr='year__gt')
  list_date_lt = django_filters.NumberFilter(field_name='listed_at', lookup_expr='year__lt')

  class Meta:
    model = Property 
    fields = ["name", "price", "location", "listed_at"]
  
class TransactionFilters(django_filters.FilterSet):
  transaction_type = django_filters.CharFilter(lookup_expr='icontains')

  class Meta:
    model = Transaction
    fields = ['transaction_type']


