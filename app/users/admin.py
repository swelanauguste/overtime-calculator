from django.contrib import admin

from .models import Department, Gender, Profile, Role

admin.site.register(Department)
admin.site.register(Gender)
admin.site.register(Profile)
admin.site.register(Role)
