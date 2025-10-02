import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
  search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
  city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
  status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
  min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
  max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
  listed_after = django_filters.DateFilter(field_name="listed_at", lookup_expr="gte")
  listed_before = django_filters.DateFilter(field_name="listed_at", lookup_expr="lte")

  class Meta:
    model = Property
    fields = [
      "search",
      "city",
      "status",
      "min_price",
      "max_price",
      "listed_after",
      "listed_before",
    ]
