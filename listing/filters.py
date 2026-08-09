import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
  search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
  city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
  status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
  listing_type = django_filters.CharFilter(field_name="listing_type", lookup_expr="iexact")
  property_type = django_filters.CharFilter(field_name="property_type", lookup_expr="iexact")
  county = django_filters.CharFilter(field_name="county", lookup_expr="icontains")
  neighborhood = django_filters.CharFilter(field_name="neighborhood", lookup_expr="icontains")
  min_bedrooms = django_filters.NumberFilter(field_name="bedrooms", lookup_expr="gte")
  max_bedrooms = django_filters.NumberFilter(field_name="bedrooms", lookup_expr="lte")
  min_bathrooms = django_filters.NumberFilter(field_name="bathrooms", lookup_expr="gte")
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
      "listing_type",
      "property_type",
      "county",
      "neighborhood",
      "min_bedrooms",
      "max_bedrooms",
      "min_bathrooms",
      "min_price",
      "max_price",
      "listed_after",
      "listed_before",
    ]
