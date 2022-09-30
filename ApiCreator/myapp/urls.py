from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.base),
    path('1', views.getDB, name='getDB'),
]