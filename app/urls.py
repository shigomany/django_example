from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('auth/', view=views.auth, name='auth'),
    path('logout/', view=views.logout_p, name='logout'),
    path('<int:pk>', view=views.add_to_cart, name='add_to_cart'),
    path('cart', view=views.cart, name='cart-detail'),
    path('cart/<int:pk>', view=views.cart_delete, name='cart-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
