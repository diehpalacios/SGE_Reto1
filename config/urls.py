# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Todo lo que empiece por /api/ irá a la oficina de agenda
    path('api/', include('agenda.urls')),

    # LA RUTA MÁGICA: La raíz ('') sirve el index.html de Vue
    path('', TemplateView.as_view(template_name='index.html')),
]