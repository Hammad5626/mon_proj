from django.contrib import admin
from .models import DataModel, UserModel

admin.site.register(DataModel)
admin.site.register(UserModel)