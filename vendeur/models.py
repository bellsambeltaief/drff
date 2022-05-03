from django.db import models
# Create your models here.


class Vendeur(models.Model):
    vend_regNo = models.TextField(unique=True)
    vend_name = models.TextField()
    vend_email = models.TextField()
    vend_mobile = models.TextField(null=True)
    