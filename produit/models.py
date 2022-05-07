from django.db import models
# Create your models here.

class Produit(models.Model):
    prod_regNo = models.CharField(unique=True, max_length=255)
    prod_name = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prod_name
