from rest_framework.permissions import BasePermission

class EsBibliotecario(BasePermission):

    """
    Permite acceso solo a bibliotecarios.
    """

    def has_permission(self, request, view):
        return request.user.role == 'bibliotecario'
    
class EsEstudianteOProfesor(BasePermission):

    """
    Permite acceso a estudiantes y profesores.
    """

    def  has_permission(self, request, view):
        return request.user.role in ['estudiante', 'profesor']
    
class EsDuenno(BasePermission):

    """
    Permite acceso solo a los dueños de la instancia.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user