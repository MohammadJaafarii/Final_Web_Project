from django.contrib import admin
from .models import ObjectStorage,CustomUser

# Register your models here.

admin.site.register(ObjectStorage)
admin.site.register(CustomUser)