from django.db import models
# Create your models here.
class Produit(models.Model):
    prod_regNo = models.TextField(unique=True)
    prod_name = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
