import pytest
from django.urls import reverse
from rest_framework import status
from biblioteca_app.models import Prestamo
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_list_prestamos(api_client, estudiante):
    api_client.force_authenticate(user=estudiante)
    url = reverse('prestamo-list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_prestamo(api_client, estudiante, prestamo):
    url = reverse('prestamo-detail', args=[prestamo.id])
    api_client.force_authenticate(user=estudiante)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_create_prestamo(api_client, estudiante, libro):
    api_client.force_authenticate(user=estudiante)
    url = reverse('prestamo-list-create')
    data = {'libro': libro.id, 'user': estudiante.id}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

