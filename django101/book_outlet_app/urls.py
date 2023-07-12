from django.urls import path
from . import views # . means same directory
from .views import (BookListApiView, BookDetailApiView)

urlpatterns = [
#     path('', views.index),
    path('', BookListApiView.as_view()),
    path('<int:book_id>', BookDetailApiView.as_view())
]

