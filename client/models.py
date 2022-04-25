from django.db import models

# Create your models here.

class Clients(models.Model):
    cl_regNo = models.TextField(unique=True)
    cl_name = models.TextField(unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    field_name = models.EmailField(max_length=254)
   
 

    #created_at = models.DateTimeField(auto_now=True)


