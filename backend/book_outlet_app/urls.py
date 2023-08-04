from django.urls import path
from . import views # . means same directory
from .views import (BookListApiView, BookDetailApiView)

urlpatterns = [
    path('', BookListApiView.as_view()),
    path('<int:book_id>', BookDetailApiView.as_view()),
    path('index', views.index),
    # path('index', BookListApiView.as_view()),
    path('api', views.api_home),
    path('api/search', views.api_search),

]

