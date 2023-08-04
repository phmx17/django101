from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.
class Library(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    short = models.CharField(max_length=4, unique=True)
    inventory = models.ForeignKey('Book', null=True, related_name='books', on_delete=models.PROTECT)

    # inventory = models.ManyToManyField(Book)
    def __str__(self):
        return f"{self.name} {self.city}"

    class Meta:
        verbose_name_plural = 'Libraries'  # shows proper spelling in admin ui


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    author = models.CharField(blank=True,
                              max_length=100)  # don't do 'null=True'
    is_bestselling = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(null=True, blank=True)
    library = models.ForeignKey(Library, null=True, related_name='books', on_delete=models.PROTECT)
    countries = models.ManyToManyField('Country')

    # custom return
    def title_and_author(self):
        return f"{self.title} by {self.author}"

    # to string method
    def __str__(self):
        return f"{self.title} by {self.author}"


class Country(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries' # shows proper spelling in admin ui
