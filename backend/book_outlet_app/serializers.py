from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Book
        fields = ['title', 'author', 'rating', 'is_bestselling', 'user', 'my_discount']

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Book):
            return None
        return obj.get_discount()
