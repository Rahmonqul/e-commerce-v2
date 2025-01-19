import django_filters
from .models import Product, VariantItem

PRODUCT_FEATURE_CHOICES = [
    ('', 'All'),
    ('best_seller', 'Best Seller'),
    ('sale', 'On Sale'),
    ('new_arrival', 'New Arrival'),
]

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__title", lookup_expr='exact', label="Category")

    # subcategory = django_filters.CharFilter(field_name="subcategory__title", lookup_expr='exact', label="Subcategory")

    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte', label="Min Price")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte', label="Max Price")

    color = django_filters.CharFilter(field_name="variant__variant_items__title", lookup_expr='icontains',
                                      label="Color")


    size = django_filters.CharFilter(field_name="variant__variant_items__title", lookup_expr='icontains', label="Size")


    style = django_filters.CharFilter(field_name="variant__variant_items__title", lookup_expr='icontains',
                                      label="Style")

    class Meta:
        model = Product
        fields = ['category', 'price_min', 'price_max', 'color', 'size', 'style']

class ProductListFilter(django_filters.FilterSet):
    # active = django_filters.BooleanFilter(field_name='product')
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