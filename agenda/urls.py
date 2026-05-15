# agenda/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, CitaViewSet, ServicioViewSet, ProfesionalViewSet, DisponibilidadViewSet

router = DefaultRouter()
router.register(r'servicios', ServicioViewSet)
router.register(r'profesionales', ProfesionalViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'disponibilidad', DisponibilidadViewSet)
router.register(r'citas', CitaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]