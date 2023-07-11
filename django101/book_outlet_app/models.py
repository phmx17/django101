from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.CharField(blank=True, max_length=100) # don't do 'Null = True' since this should be an empty string; A Null value will be written for other types
    is_bestselling = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.title} ({self.rating}) author: {self.author}'