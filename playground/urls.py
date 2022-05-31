from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.getStatus),
    path('active/', views.activate)
]