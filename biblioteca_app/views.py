from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from biblioteca_app.models import Libro, Prestamo, Reserva, Valoracion
from biblioteca_app.serializers import CustomUserSerializer, LibroSerializer, PrestamoSerializer, ReservaSerializer, ValoracionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import EsBibliotecario, EsEstudianteOProfesor, EsDuenno
from rest_framework import status
from biblioteca_app.filters import LibroFilter, ReservaFilter, PrestamoFilter
from django_filters.rest_framework import DjangoFilterBackend
from notificaciones.utils import enviar_correo_prestamo, enviar_correo_reserva

User = get_user_model()

class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        if self.request.method == 'GET':
            return [IsAuthenticated(), EsBibliotecario()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        role = request.data.get("role")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Nombre de usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Correo electrónico ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        if username and password and email and role:
            user = User.objects.create_user(username=username, password=password, email=email, role=role)
            return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Faltan datos"}, status=status.HTTP_400_BAD_REQUEST)
    
#CRUD PARA LIBRO
class LibroListCreate(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LibroFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            # Solo bibliotecarios pueden crear libros
            return [IsAuthenticated(), EsBibliotecario()]
        # Todos los usuarios autenticados pueden ver la lista de libros
        return [IsAuthenticated()]

class LibroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            #Todos los usuarios autenticados pueden ver el libro
            return [IsAuthenticated()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            #Solo los bibliotecarios pueden actualizar o eliminar un libro
            return [IsAuthenticated(), EsBibliotecario()]

#CRUD PARA PRESTAMO
class PrestamoListCreate(generics.ListCreateAPIView):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrestamoFilter
    
    def get_permissions(self):
        if self.request.method == 'POST':
            # Solo estudiantes y profesores pueden crear prestamos
            return [IsAuthenticated(), EsEstudianteOProfesor()]
        # Todos los usuarios autenticados pueden ver la lista de prestamos
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        prestamo = serializer.save(user=self.request.user)
        enviar_correo_prestamo(prestamo.user, prestamo.libro)

class PrestamoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            #Todos los usuarios autenticados pueden ver el prestamo
            return [IsAuthenticated()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            #Solo los estudiantes y profesores pueden actualizar o eliminar su propio prestamo
            return [IsAuthenticated(), EsDuenno()]

#CRUD PARA RESERVA
class ReservaListCreate(generics.ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservaFilter
    
    def get_permissions(self):
        if self.request.method == 'POST':
            # Solo estudiantes y profesores pueden crear reservas
            return [IsAuthenticated(), EsEstudianteOProfesor()]
        # Todos los usuarios autenticados pueden ver la lista de reservas
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        reserva = serializer.save(user=self.request.user)
        enviar_correo_prestamo(reserva.user, reserva.libro)

class ReservaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            #Todos los usuarios autenticados pueden ver la reserva
            return [IsAuthenticated()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            #Solo los estudiantes y profesores pueden actualizar o eliminar su propia reserva
            return [IsAuthenticated(), EsDuenno()]

#CRUD PARA VALORACION
class ValoracionListCreate(generics.ListCreateAPIView):
    queryset = Valoracion.objects.all()
    serializer_class = ValoracionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # Solo estudiantes y profesores pueden crear valoraciones
            return [IsAuthenticated(), EsEstudianteOProfesor()]
        # Todos los usuarios autenticados pueden ver la lista de valoraciones
        return [IsAuthenticated()]

class ValoracionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Valoracion.objects.all()
    serializer_class = ValoracionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            #Todos los usuarios autenticados pueden ver la valoracion
            return [IsAuthenticated()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            #Solo los estudiantes y profesores pueden actualizar o eliminar su propia valoracion
            return [IsAuthenticated(), EsDuenno()]