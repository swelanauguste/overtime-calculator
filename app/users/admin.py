from django.contrib import admin

from .models import Department, Gender, Profile, Role, User

admin.site.register(Department)
admin.site.register(Gender)
admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(User)
