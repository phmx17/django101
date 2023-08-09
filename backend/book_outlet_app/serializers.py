from rest_framework import serializers
from .models import Book, Library
from . import validators
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[UniqueValidator(queryset=Book.objects.all())])  # use custom validators
    author = serializers.CharField(validators=[validators.no_hello])  # reuse my custom validator

    class Meta:
        model = Book
        fields = ['title', 'author', 'rating', 'is_bestselling', 'file']


class TitleSearchSerializer(serializers.ModelSerializer):
    # find book with title

    class Meta:
        model = Book
        fields = ['title']


class LibrarySerializer(serializers.ModelSerializer):
    # optional custom validators here
    class Meta:
        model = Library
        fields = ['name', 'city', 'short', 'state']


''' simple jwt serializer which gets called in settings.py '''

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token
