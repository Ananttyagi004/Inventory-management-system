from django.db import models

# Create your models here.
from django.db import models

class Item(models.Model):
    sku = models.CharField(max_length=20, primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
