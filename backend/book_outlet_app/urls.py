from django.urls import path
from . import views
from .views import (BookListApiView, BookDetailApiView, BookList)

urlpatterns = [
    path('index', BookList.as_view(), name='book-list'),
    path('<int:book_id>', BookDetailApiView.as_view()), # as_view() converts class based to function based
    path('search', views.api_search),
    # path('', views.api_home), # to be removed
    # path('index', views.index),

]

