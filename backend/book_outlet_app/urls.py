from django.urls import path
from . import views # . means same directory
from .views import (BookListApiView, BookDetailApiView)

urlpatterns = [
    path('index', BookListApiView.as_view()),
    path('<int:book_id>', BookDetailApiView.as_view()), # as_view() converts class based to function based
    path('search', views.api_search),
    # path('', views.api_home), # to be removed
    # path('index', views.index),

]

