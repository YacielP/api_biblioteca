from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Rutas para libros
    path('libros/', views.LibroListCreate.as_view(), name='libro-list-create'),
    path('libros/<int:pk>/', views.LibroDetail.as_view(), name='libro-detail'),

    # Rutas para préstamos
    path('prestamo/', views.PrestamoListCreate.as_view(), name='prestamo-list-create'),
    path('prestamo/<int:pk>/', views.PrestamoDetail.as_view(), name='prestamo-detail'),

    # Rutas para valoraciones
    path('valoracion/', views.ValoracionListCreate.as_view(), name='valoracion-list-create'),
    path('valoracion/<int:pk>/', views.ValoracionDetail.as_view(), name='valoracion-detail'),

    # Rutas para reservas
    path('reserva/', views.ReservaListCreate.as_view(), name='reserva-list-create'),
    path('reserva/<int:pk>/', views.ReservaDetail.as_view(), name='reserva-detail'),

    # Rutas para autenticación
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
