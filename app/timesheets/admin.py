from django.contrib import admin

from .models import OvertimeRate, TimeSheet

admin.site.register(TimeSheet)
admin.site.register(OvertimeRate)
