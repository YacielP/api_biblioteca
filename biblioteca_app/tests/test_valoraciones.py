import pytest
from rest_framework import status
from django.urls import reverse
from biblioteca_app.models import Valoracion
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_list_valoracion(api_client, bibliotecario):
    api_client.force_authenticate(bibliotecario)
    url = reverse('valoracion-list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_valoracion(api_client, profesor, libro):
    api_client.force_authenticate(profesor)
    url = reverse('valoracion-list-create')
    data = {'user': profesor.id, 'libro': libro.id, 'comentario': "Muy bueno", 'resenna': 4}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_delete_valoracion(api_client, estudiante, valoracion):
    api_client.force_authenticate(estudiante)
    url = reverse('valoracion-detail', args=[valoracion.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT