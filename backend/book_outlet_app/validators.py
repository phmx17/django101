from rest_framework import serializers
from .models import Book
from rest_framework.validators import UniqueValidator


# custom validator for unique title
def validate_title(value):
    qs = Book.objects.filter(title__iexact=value)
    if qs.exists():
        raise serializers.ValidationError(f"The title of {value} is already in use.")

    return value

def validate_no_hello(value):
    if 'hello' in value.lower():
        raise serializers.ValidationError(f"This field does not allow the word '{value}'")
    return value


# DRF built-in validator for unique title: UniqueValidator()
unique_book_title = UniqueValidator(queryset=Book.objects.all())
