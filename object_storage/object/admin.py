from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TempUser,ObjectStorage,CustomUser
# Register your models here.

admin.site.register(ObjectStorage)
admin.site.register(CustomUser)
admin.site.register(TempUser)

