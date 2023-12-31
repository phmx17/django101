from django.urls import path
from . import views
from .views import (BookListApiView, BookDetailApiView, BookList, BookSingle, GenericBookList, GenericBookDetail)

urlpatterns = [
    # my auth paths
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('test/', views.test, name='test'),
    path('not_authorized/', views.not_authorized, name='not_authorized'),

]

