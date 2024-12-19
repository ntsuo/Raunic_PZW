from django.contrib import admin
from main.models import *
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass

model_list= [Umjetnik, Djelo, KulturniDogadaj]
admin.site.register(model_list)

