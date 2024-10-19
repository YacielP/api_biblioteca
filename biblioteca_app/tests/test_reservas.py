import pytest
from django.urls import reverse
from rest_framework import status
from biblioteca_app.models import Reserva
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_list_reserva(api_client, estudiante):
    api_client.force_authenticate(user=estudiante)
    url = reverse('reserva-list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_reserva(api_client, profesor, libro):
    api_client.force_authenticate(profesor)
    url = reverse('prestamo-list-create')
    data = {'libro': libro.id, 'user': profesor.id}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_delete_reserva(api_client, estudiante, reserva):
    api_client.force_authenticate(estudiante)
    url = reverse('reserva-detail', args=[reserva.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT