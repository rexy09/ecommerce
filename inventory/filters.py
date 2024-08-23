import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter()
    category = django_filters.NumberFilter()

    class Meta:
        model = Product
        fields = {
            'created_at': ['date__gte', 'date__lte'],
            'price': ['gte', 'lte'],
        }
