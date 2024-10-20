import django_filters
from biblioteca_app.models import Libro

class LibroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    autor = django_filters.CharFilter(lookup_expr='icontains')
    anno_escrito = django_filters.NumberFilter()

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'anno_escrito']