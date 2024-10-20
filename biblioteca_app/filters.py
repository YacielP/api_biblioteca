import django_filters
from biblioteca_app.models import Libro, Reserva

class LibroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    autor = django_filters.CharFilter(lookup_expr='icontains')
    anno_escrito = django_filters.NumberFilter()

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'anno_escrito']

class ReservaFilter(django_filters.FilterSet):
    estado = django_filters.CharFilter(lookup_expr='icontains')
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = Reserva
        fields = ['estado', 'user']