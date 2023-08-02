from django.contrib import admin
from .models import Book, Library, Country, TimeUser, TimeProject, TimeAllocation


# Register your models here.
class TimeUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_admin') # filter in right panel
    list_filer = ('name', 'is_admin') # show cols
class TimeProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name') # filter in right panel
    list_filer = ('title', 'company_name') # show cols

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('user', ) # tuple
    list_filter = ('author', 'rating', 'is_bestselling') # filter in right panel
    list_display = ('title', 'author', 'library') # show cols

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
admin.site.register(TimeUser, TimeUserAdmin)
admin.site.register(TimeProject, TimeProjectAdmin)
admin.site.register(TimeAllocation)
