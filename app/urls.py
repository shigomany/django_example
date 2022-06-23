from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('auth/', view=views.auth, name='auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
