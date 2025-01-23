import django_filters
from .models import Product

PRODUCT_FEATURE_CHOICES = [
    ('', 'All'),
    ('best_seller', 'Best Seller'),
    ('sale', 'On Sale'),
    ('new_arrival', 'New Arrival'),
]
class ProductFilter(django_filters.FilterSet):
    color = django_filters.CharFilter(method='filter_by_variant', label="Color")
    size = django_filters.CharFilter(method='filter_by_variant', label="Size")
    style = django_filters.CharFilter(method='filter_by_variant', label="Style")
    min_price = django_filters.NumberFilter(method='filter_by_price', label="Min Price")
    max_price = django_filters.NumberFilter(method='filter_by_price', label="Max Price")

    class Meta:
        model = Product
        fields = ['color', 'size', 'style', 'min_price', 'max_price']

    def filter_by_variant(self, queryset, name, value):
        """
        Фильтрует продукты на основе значений вариантов (цвет, размер, стиль).
        """
        filter_kwargs = {
            f'variant__{name}__name__icontains': value
        }
        return queryset.filter(**filter_kwargs).distinct()

    def filter_by_price(self, queryset, name, value):

        if name == 'min_price':
            return queryset.filter(variant__price_variant__gte=value).distinct()
        elif name == 'max_price':
            return queryset.filter(variant__price_variant__lte=value).distinct()
        return queryset


class ProductListFilter(django_filters.FilterSet):
    product_feature = django_filters.ChoiceFilter(
        label='Product Feature',
        choices=PRODUCT_FEATURE_CHOICES,
        method='filter_by_feature'
    )

    class Meta:
        model = Product
        fields = ['product_feature']

    def filter_by_feature(self, queryset, name, value):
        if value == 'best_seller':
            return queryset.filter(best_seller=True)
        elif value == 'sale':
            return queryset.filter(sale=True)
        elif value == 'new_arrival':
            return queryset.filter(new_arrival=True)
        return queryset