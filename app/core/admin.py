from django.contrib import admin

from .models import Department, Role, TimeSheet

admin.site.register(TimeSheet)
admin.site.register(Role)
admin.site.register(Department)

