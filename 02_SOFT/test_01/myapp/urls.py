from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('admin', views.hello),
    path('about/', views.about),
]
