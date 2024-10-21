from rest_framework import generics
from biblioteca_app.models import Libro, Prestamo, Reserva, Valoracion
from biblioteca_app.serializers import LibroSerializer, PrestamoSerializer, ReservaSerializer, ValoracionSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import EsBibliotecario, EsEstudianteOProfesor, EsDuenno
from notificaciones.utils import enviar_correo_prestamo, enviar_correo_devolucion, enviar_correo_reserva

#CRUD PARA LIBRO
class LibroListCreate(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

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
    
    def get_permissions(self):
        if self.request.method == 'POST':
            # Solo estudiantes y profesores pueden crear reservas
            return [IsAuthenticated(), EsEstudianteOProfesor()]
        # Todos los usuarios autenticados pueden ver la lista de prestamos
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        reserva = serializer.save(user=self.request.user)
        enviar_correo_reserva(reserva.user, reserva.libro)

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