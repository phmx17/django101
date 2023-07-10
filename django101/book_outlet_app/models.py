from django.db import models

# Create your models here.

class Book(models.py):
    title = models.Charfield(max_length=50)
    rating = models.Integerfield()