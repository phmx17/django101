from django.urls import path
from . import views # . means same directory
from .views import (BookListApiView, BookDetailApiView, TimeDetailApiView)

urlpatterns = [
#     path('', views.index),
    path('', BookListApiView.as_view()),
    path('<int:book_id>', BookDetailApiView.as_view()),
    path('index', views.index),
    path('api', views.api_home),
    path('api/search', views.api_search),
    path('api/timeboss', views.api_time_boss),
    path('api/timeboss/projects', views.api_time_boss_projects),
    path('api/timeboss/allocations', views.api_time_boss_allocations)

]

