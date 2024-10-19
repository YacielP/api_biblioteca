from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('bibliotecario', 'Bibliotecario'),
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    anno_escrito = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)  # Se asume que inicialmente está disponible
    devolucion = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='libros_ocupados')
    resenna_Total = models.FloatField(validators=[MinValueValidator(0)], default=0)
    resenna_cant = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if self.user:
            self.disponible = False
        else:
            self.disponible = True
            self.devolucion = None  # Elimina la fecha de devolución si no está ocupado
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['titulo']

class Prestamo(models.Model):
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.fecha_prestamo:
            self.fecha_prestamo = timezone.now()
        if not self.fecha_devolucion:
            self.fecha_devolucion = self.fecha_prestamo + timedelta(days=14)
        self.libro.devolucion = self.fecha_devolucion
        self.libro.user = self.user
        self.libro.disponible = False
        self.libro.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"El libro {self.libro} está siendo usado por {self.user.username}"




class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=100, choices=ESTADO_CHOICES, default='activa')
    fecha_expiracion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"El usuario {self.user.username} tiene una reserva para el libro {self.libro.titulo}"

    def save(self, *args, **kwargs):
        if self.libro.devolucion:
            self.fecha_expiracion = self.libro.devolucion + timedelta(days=1)
        super().save(*args, **kwargs)

class Valoracion(models.Model):
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True, null=True, validators=[MinLengthValidator(5), MaxLengthValidator(500)])
    resenna = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        suma_prom = self.libro.resenna_Total * self.libro.resenna_cant
        nueva_suma_prom = suma_prom + self.resenna
        self.libro.resenna_cant += 1
        self.libro.resenna_Total = nueva_suma_prom / self.libro.resenna_cant
        self.libro.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"El usuario {self.user.username} realizo una valoracion al libro {self.libro.titulo}"