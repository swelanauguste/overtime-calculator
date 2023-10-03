from django.urls import path

from .views import TimeSheetDetailView, TimeSheetListView, create_time_sheet, export_to_csv

urlpatterns = [
    path("", TimeSheetListView.as_view(), name="timesheet-list"),
    path("detail/<int:pk>/", TimeSheetDetailView.as_view(), name="timesheet-detail"),
    path("create/", create_time_sheet, name="timesheet-create"),
    path('export/', export_to_csv, name='export_timesheets'),
]
