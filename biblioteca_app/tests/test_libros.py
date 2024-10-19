import pytest
from django.urls import reverse
from rest_framework import status
from biblioteca_app.models import Libro
from django.contrib.auth import get_user_model

User = get_user_model

@pytest.mark.django_db
def test_list_libros(api_client, estudiante):
    api_client.force_authenticate(user=estudiante)
    url = reverse('libro-list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_libro_as_bibliotecario(api_client, bibliotecario):
    api_client.force_authenticate(user=bibliotecario)
    url = reverse('libro-list-create')
    data = {'titulo': 'Nuevo Libro', 'autor': 'Autor Ejemplo', 'anno_escrito': 2022}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_create_libro_as_estudiante(api_client, estudiante):
    api_client.force_authenticate(user=estudiante)
    url = reverse('libro-list-create')
    data = {'titulo': 'Nuevo Libro', 'autor': 'Autor Ejemplo', 'anno_escrito': 2022}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_delete_libro_as_bibliotecario(api_client, bibliotecario, libro):
    url = reverse('libro-detail', args=[libro.id])
    api_client.force_authenticate(user=bibliotecario)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
