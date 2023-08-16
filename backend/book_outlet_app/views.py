from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, HttpRequest
from django.forms.models import model_to_dict  # alternative to serializer
from django.urls import reverse
from rest_framework.views import APIView  # class views
from rest_framework.decorators import api_view  # @decorator
from rest_framework.response import Response  # built into the decorator
from rest_framework import status, permissions, mixins, generics
from django.shortcuts import get_object_or_404, render, redirect  # 404 == great shortcut
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # JWT auth

from .models import Book
from .serializers import BookSerializer
from .forms import CreateUserForm
from .decorators import unauthenticated_user

''' JWT authorization views '''

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.name  # this is my custom entry into the token
        return token

''' implementing my way of using local django to authenticate'''

@unauthenticated_user
def register(request):
    template = 'auth/register.html'
    form = CreateUserForm()  # initialize
    # use same route to return post data
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():  # own serializer
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {user}.")  # print success message
            return redirect('login')
    context = {'form': form}
    return render(request, template, context)

@unauthenticated_user
def login_page(request):
    template = 'auth/login.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('test')
        else:
            messages.info(request, 'Incorrect username or password.')
    context = {}
    return render(request, template, context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login') # immediate redirect if not authenticated
def test(request):
    template = 'auth/test.html'
    title = "Movie Titles"
    films = ['titanic', 'the abyss', 'the terminator']
    context = {'title': title, 'films': films}
    return render(request, template, context)

''' this demontrates using generics which seem to be the simplest '''

class GenericBookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class GenericBookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

''' this demontrates using mixins with generic views '''

class BookList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class BookSingle(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, **kwargs):
        return self.retrieve(request)

    def put(self, request, **kwargs):
        return self.update(request)

'''ListApiView;  this could be rolled into the CreateApiView'''

class BookListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # add permission to check if user is authenticated

    # 1. List all books
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# BookDetailApiView
class BookDetailApiView(APIView):
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
        book_instance = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

# standard controllers
# @api_view(['GET'])
# def index(request):
#     books = Book.objects.all()
#     serializer = BookSerializer(books, many=True)
#     # print('serializer: : ', serializer.data)
#     return Response({'books': serializer.data})


# @api_view(['POST'])  # make this into a DRF view
# def api_home(request):
#     print("request method", request.method)
#     serializer = BookSerializer(data=request.data)
#     if serializer.is_valid(
#             raise_exception=True):  # raise_exception will return detailed error like "...this field is required"
#         #         instance = serializer.save() # return obj class of models; use the instance for ingesting data
#         #         instance = form.save() # similar
#         # print("serializer is valid. Title to be saved:", request.data['title'])
#         serializer.save()
#         return Response(serializer.data)  # can't return instance since it cannot be serialized
#
#     return Response({'invalid': 'not good data'}, status=400)

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
# @api_view(['GET', 'POST'])
# def api_time_boss(request: HttpRequest):
#     # get all users
#     time_users = TimeUser.objects.all()
#
#     print(time_users.values_list('name', 'id', named=True))
#
#     return Response({'users': time_users.values_list('name', 'id')}) # return possible as serialized
#
#     # this is for dev name input autocomplete
#     if request.method == 'POST':
#         requested_user = request.data['requestedUser']
#         user_query = TimeUser.objects.filter(name__contains=requested_user)
#         # user_results = []
#         # for user in user_query:
#         #     user_results.append(user.name)
#         print("user_results", user_results)
#
#         return Response({'user_query': user_query.values_list('name')})
#
# @api_view(['GET', 'POST'])
# def api_time_boss_projects(request):
#     time_projects = TimeProject.objects.all()
#     # requested_title = request.data['titleInput']
#     # title_query = Book.objects.filter(title__contains=requested_title)
#     index_projects = []
#     for project in time_projects:
#         index_projects.append(project.title)
#     print("index_projects: ", index_projects)
#
#     return Response({'users': index_projects})
#
#     if request.method == 'POST':
#         requested_user = request.data['requestedUser']
#         user_query = TimeUser.objects.filter(name__contains=requested_user)
#         # user_results = []
#         # for user in user_query:
#         #     user_results.append(user.name)
#         print("user_results", user_results)
#
#         return Response({'user_query': user_query.values_list('name')})
#
# @api_view(['GET', 'POST'])
# def api_time_boss_allocations(request):
#     allocations = TimeAllocation.objects.all()
#
#     return Response({'allocations': allocations.values('developer', 'date', 'time', 'comment', 'timerTotalTime' )})
#
# # post new entry
#     if request.method == 'POST':
#         serializer = AllocationSerializerSerializer(data=request.data)
#         if serializer.is_valid(
#                 raise_exception=True):  # raise_exception will return detailed error like "...this field is required"
#
#             serializer.save()
#             return Response({"entry": user_query.values(serializer.data)})  # can't return instance since it cannot be serialized
#
#         return Response({'invalid': 'not good data'}, status=400)
#


# left overs
#     if month in monthlyChallenges:
#         return JsonResponse({'challenge': monthlyChallenges[month]})
#         return HttpResponse(f'Your challenge for {month} is: {monthlyChallenges[month]}')
