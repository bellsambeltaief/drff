from django.contrib import admin
from .models import Clients
# Register your models here.

@admin.register(Clients)
class ClientAdmin (admin.ModelAdmin):
    list_display = ['id', 'cl_name', 'cl_regNo', 'firstname', 'lastname', 'password', 'field_name']