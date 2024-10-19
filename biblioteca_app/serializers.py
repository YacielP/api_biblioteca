from rest_framework import serializers
from django.contrib.auth import get_user_model
from biblioteca_app.models import Libro, Valoracion, Reserva, Prestamo

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'anno_escrito', 'disponible', 'devolucion', 'resenna_Total', 'resenna_cant']

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = ['id', 'libro', 'user', 'fecha_prestamo', 'fecha_devolucion']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'user', 'libro', 'fecha_reserva', 'estado', 'fecha_expiracion']

class ValoracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valoracion
        fields = ['id', 'libro', 'user', 'comentario', 'resenna']
