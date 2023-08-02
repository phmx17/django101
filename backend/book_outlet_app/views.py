from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, HttpRequest
from django.forms.models import model_to_dict  # alternative to serializer
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view

# get user model
from django.contrib.auth import get_user_model

from .models import Book, TimeUser, TimeProject, TimeAllocation
from .serializers import BookSerializer, AllocationSerializer


# Create your views here.
# class views
class TimeDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # get single record by book id and user id
    def get_object(self, book_id, user_id):
        try:
            return Book.objects.get(id=book_id, user=user_id)
        except Book.DoesNotExist:
            return None

    # retrieve book by given id
    def get(self, request, book_id, *args, **kwargs):
        book_instance = self.get_object(book_id, request.user.id)  # self is the instance
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
        serializer = BookSerializer(instance=book_instance, data=data, partial=True)
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
# ListApiView;  this could be rolled into the CreateApiView
class BookListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all books by user
    def get(self, request, *args, **kwargs):
        books = Book.objects.filter(user=request.user.id)
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
        print("POST data: ", data)

        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            #             instance = serializer.save() # create an instance
            #             instance = form.save() # create an instance

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# BookDetailApiView
class BookDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # get single record by book id and user id
    def get_object(self, book_id, user_id):
        try:
            return Book.objects.get(id=book_id, user=user_id)
        except Book.DoesNotExist:
            return None

    # retrieve book by given id
    def get(self, request, book_id, *args, **kwargs):
        book_instance = self.get_object(book_id, request.user.id)  # self is the instance
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
        serializer = BookSerializer(instance=book_instance, data=data, partial=True)
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
    return JsonResponse({'books': serializer.data})


@api_view(['POST'])  # make this into a DRF view
def api_home(request):
    print("request method", request.method)
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid(
            raise_exception=True):  # raise_exception will return detailed error like "...this field is required"
        #         instance = serializer.save() # return obj class of models; use the instance for ingesting data
        #         instance = form.save() # similar
        # print("serializer is valid. Title to be saved:", request.data['title'])
        serializer.save()
        return Response(serializer.data)  # can't return instance since it cannot be serialized

    return Response({'invalid': 'not good data'}, status=400)

# Search
@api_view(['POST'])
def api_search(request):
    requested_title = request.data['titleInput']
    title_query = Book.objects.filter(title__contains=requested_title)
    title_results = []
    for title in title_query:
        title_results.append(title.title)
    print("title_results", title_results)

    return Response({'titleResults': title_results})


# Timeboss
@api_view(['GET', 'POST'])
def api_time_boss(request: HttpRequest):
    # get all users
    time_users = TimeUser.objects.all()

    print(time_users.values_list('name', 'id', named=True))

    return Response({'users': time_users.values_list('name', 'id')}) # return possible as serialized

    # this is for dev name input autocomplete
    if request.method == 'POST':
        requested_user = request.data['requestedUser']
        user_query = TimeUser.objects.filter(name__contains=requested_user)
        # user_results = []
        # for user in user_query:
        #     user_results.append(user.name)
        print("user_results", user_results)

        return Response({'user_query': user_query.values_list('name')})

@api_view(['GET', 'POST'])
def api_time_boss_projects(request):
    time_projects = TimeProject.objects.all()
    # requested_title = request.data['titleInput']
    # title_query = Book.objects.filter(title__contains=requested_title)
    index_projects = []
    for project in time_projects:
        index_projects.append(project.title)
    print("index_projects: ", index_projects)

    return Response({'users': index_projects})

    if request.method == 'POST':
        requested_user = request.data['requestedUser']
        user_query = TimeUser.objects.filter(name__contains=requested_user)
        # user_results = []
        # for user in user_query:
        #     user_results.append(user.name)
        print("user_results", user_results)

        return Response({'user_query': user_query.values_list('name')})

@api_view(['GET', 'POST'])
def api_time_boss_allocations(request):
    allocations = TimeAllocation.objects.all()

    return Response({'allocations': allocations.values('developer', 'date', 'time', 'comment', 'timerTotalTime' )})

# post new entry
    if request.method == 'POST':
        serializer = AllocationSerializerSerializer(data=request.data)
        if serializer.is_valid(
                raise_exception=True):  # raise_exception will return detailed error like "...this field is required"

            serializer.save()
            return Response({"entry": user_query.values(serializer.data)})  # can't return instance since it cannot be serialized

        return Response({'invalid': 'not good data'}, status=400)







# left overs
#     if month in monthlyChallenges:
#         return JsonResponse({'challenge': monthlyChallenges[month]})
#         return HttpResponse(f'Your challenge for {month} is: {monthlyChallenges[month]}')

