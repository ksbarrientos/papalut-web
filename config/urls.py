from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from catalogo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('herramientas/', views.calculadoras, name='calculadoras'),
    path('producto/<slug:slug>/', views.detalle_producto, name='detalle_producto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
