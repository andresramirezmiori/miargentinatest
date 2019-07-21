from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from exercise import views
from exercise.api import UsuarioArgenitnaViewSet

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/crear/', views.user_create, name='user_create'),
    path('usuarios/<pk>/actualizar/', views.user_update, name='user_update'),
    path('usuarios/<pk>/', views.user_detail, name='user_detail'),
]

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioArgenitnaViewSet)

urlpatterns += [
    url(r'^api/', include(router.urls)),
]
