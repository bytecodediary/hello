import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(lookup_expr='icontains')
  price = django_filters.NumberFilters()
  price_gte = django_filters.NumberFilters(field_name="price", lookup_expr='gte')
  price_lte = django_filters.NumberFilters(field_name="price", lookup_expr='lte  ')
  location = django_filters.CharFilters(lookup_fields='icontains')

  class Meta:
    model = Property 
    fields = ["name", "price", "location"]
  

