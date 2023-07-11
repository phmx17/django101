from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Book
from .serializers import BookSerializer

# Create your views here.

def index(request):

#     if month in monthlyChallenges:
#         return JsonResponse({'challenge': monthlyChallenges[month]})
#         return HttpResponse(f'Your challenge for {month} is: {monthlyChallenges[month]}')
    books = Book.objects.all()
    booksSerialized = BookSerializer(books, many=True)
    print('books serialized: ', booksSerialized.data)
    return JsonResponse({'books': booksSerialized.data })

