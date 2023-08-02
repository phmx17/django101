from rest_framework import serializers
from .models import Book, Library
from .validators import validate_title
from . import validators


class AllocationSerializer(serializers.ModelSerializer):
    # custom validation checks

    # timerTotalTime = # this would be a calculated field done here

    class Meta:
        model = Book
        fields = ['developer', 'date', 'time', 'comment', 'timerTotalTime']


class BookSerializer(serializers.ModelSerializer):
    # custom validation checks
    title = serializers.CharField(validators=[validate_title])  # uses a custom validator
    title = serializers.CharField(
        validators=[validators.unique_book_title, validators.validate_no_hello])  # use my 2 custom validators
    author = serializers.CharField(validators=[validators.validate_no_hello])  # reuse my custom validator

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
        fields = ['name', 'city', 'short', 'file']
