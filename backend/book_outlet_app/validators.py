from rest_framework import serializers
from .models import Book
from rest_framework.validators import UniqueValidator

# DRF built-in validator for unique title: UniqueValidator()
unique_book_title = UniqueValidator(queryset=Book.objects.all())


# custom validator for unique title
def title_unique(value):
    qs = Book.objects.filter(title__iexact=value)
    if qs.exists():
        raise serializers.ValidationError(f"The title of {value} is already in use.")

    return value


def no_hello(value):
    if 'hello' in value.lower():
        raise serializers.ValidationError(f"This field does not allow the word 'hello'")
    return value
