from django.contrib import admin
from .models import Book, Library, Country


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)  # tuple
    list_filter = ('author', 'rating', 'is_bestselling')  # filter in right panel
    list_display = ('title', 'author', 'library')  # show cols


class LibraryAdmin(admin.ModelAdmin):
    list_filter = ('name', 'city')
    list_display = ('name', 'city')


class CountryAdmin(admin.ModelAdmin):
    list_filter = ('name', 'region')
    list_display = ('name', 'region')


#     prepopulated_fields = {"title",}
#     list_filter = ("author", "rating")


admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Country, CountryAdmin)

