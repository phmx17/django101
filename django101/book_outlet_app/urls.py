from django.urls import path
from . import views # . means same directory

urlpatterns = [
    path('', views.index),

]