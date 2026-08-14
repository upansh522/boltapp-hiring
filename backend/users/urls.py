from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('recognize', views.recognize, name='recognize'),
    path('verify', views.verify, name='verify'),
]