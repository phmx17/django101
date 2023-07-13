from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    author = models.CharField(blank=True, max_length=100) # don't do 'null=True' since this should be an empty string; A Null value will be written for other types
    is_bestselling = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    @property
    def sale_price(self):
        return "this is calling sale_price..."
    def get_discount(self):
        return "this is calling get_discount"



    def __str__(self):
        return f'{self.title} ({self.user})'