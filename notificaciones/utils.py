"""
    AQUI SE DEFINEN LAS FUNCIONES
    PARA ENVIAR CORREO
"""

from django.core.mail import send_mail
from django.conf import settings

def enviar_correo_reserva(usuario, libro):
    asunto = 'Reserva del libro confirmada'
    mensaje = f'Hola, {usuario.username}, \n\nHas reservado el libro "{libro.titulo}"'
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [usuario.email])

def enviar_correo_prestamo(usuario, libro):
    asunto = 'Prestamo del Libro Confirmado'
    mensaje = f'Hola, {usuario.username}, \n\nHas tomado prestado el libro "{libro.titulo}"'
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [usuario.email])