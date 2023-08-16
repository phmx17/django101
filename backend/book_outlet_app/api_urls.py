from django.urls import path
from . import views
from .views import (BookListApiView, BookDetailApiView, BookList, BookSingle, GenericBookList, GenericBookDetail)

urlpatterns = [
    path('index/', GenericBookList.as_view(), name='book-list'),
    # path('<int:book_id>', BookDetailApiView.as_view()), # as_view() converts class based to function based
    path('single/<int:pk>', GenericBookDetail.as_view(), name='book-single'), # as_view() converts class based to function based
    # path('<int:pk>', BookSingle.as_view(), name = 'book-single'), # as_view() converts class based to function based
    path('search', views.api_search),
    # path('', views.api_home), # to be removed
    # path('index', views.index),

]

