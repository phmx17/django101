from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict # alternative to serializer
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view

from .models import Book
from .serializers import BookSerializer

# Create your views here.
# class views
class BookListApiView(APIView):
   # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all books by user
    def get(self, request, *args, **kwargs):
        books = Book.objects.filter(user = request.user.id)
#         books = model_to_dict(books) # like serializer but not as flexible;
#         return Response(books, status=status.HTTP_200_OK) # must use JsonResponse
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # assemble data package
        data = {
            'title': request.data.get('title'),
            'author': request.data.get('author'),
            'rating': request.data.get('rating'),
            'user': request.user.id
        }

        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
#             instance = serializer.save() # create an instance
#             instance = form.save() # create an instance

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(booksSerialized.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailApiView(APIView):
   # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # get single record by book id and user id
    def get_object(self, book_id, user_id):
        try:
            return Book.objects.get(id=book_id, user = user_id)
        except Book.DoesNotExist:
            return None

    # retrieve book by given id
    def get(self, request, book_id, *args, **kwargs):
        book_instance = self.get_object(book_id, request.user.id) # self is the instance
        if not book_instance:
            return Response(
                {"res": "Object with book id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booksSerialized = BookSerializer(book_instance)
        return Response(booksSerialized.data, status=status.HTTP_200_OK)

   # update a single record
    def put(self, request, book_id, *args, **kwargs):
        book_instance = self.get_object(book_id, request.user.id)
        if not book_instance:
            return Response(
                {"res": "Object with book id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # assemble data package
        data = {
            'book': request.data.get('book'),
            'author': request.data.get('author'),
            'rating': request.data.get('rating'),
            'user': request.user.id
        }
        # serialize
        serializer = BookSerializer(instance = book_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete single book
    def delete(self, request, book_id, *args, **kwargs):
        book_instance = self.get_object(book_id, request.user.id)
        if not book_instance:
            return Response(
                {"res": "Object with book id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        book_instance.delete()
        return Response(
            {"res": "Book deleted!"},
            status=status.HTTP_200_OK
        )


# standard controller
def index(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    print('serializer: : ', serializer.data)
    return JsonResponse({'books': serializer.data })

@api_view(['POST']) # make this into a DRF view
def api_home(request):
#     data = request.data
#     print(data)
#     return Response(data)
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save() # return obj class of models
#           instance = form.save() # similar
        print("instance: ", instance)

        return Response(serializer.data) # can't return instance since it cannot be serialized

    return Response({'invalid': 'not good data'}, status=400)


# left overs
#     if month in monthlyChallenges:
#         return JsonResponse({'challenge': monthlyChallenges[month]})
#         return HttpResponse(f'Your challenge for {month} is: {monthlyChallenges[month]}')
