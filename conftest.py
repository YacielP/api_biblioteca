import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from biblioteca_app.models import Libro, Valoracion, Reserva, Prestamo

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def bibliotecario(db):
    return User.objects.create_user(username='bib1', password='password123', role='bibliotecario')

@pytest.fixture
def estudiante(db):
    return User.objects.create_user(username='est1', password='password123', role='estudiante')

@pytest.fixture
def profesor(db):
    return User.objects.create_user(username='prof1', password='password123', role='profesor')

@pytest.fixture
def libro(db):
    return Libro.objects.create(titulo='El Quijote', autor='Cervantes', anno_escrito=1605)

@pytest.fixture
def valoracion(db, estudiante, libro):
    return Valoracion.objects.create(user=estudiante, libro=libro, resenna=3)

@pytest.fixture
def reserva(db, estudiante, libro):
    return Reserva.objects.create(user=estudiante, libro=libro)

@pytest.fixture
def prestamo(db, estudiante, libro):
    return Prestamo.objects.create(user=estudiante, libro=libro)