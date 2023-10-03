from django.urls import path

from .views import (
    TimeSheetCreateView,
    TimeSheetDetailView,
    TimeSheetListView,
    TimeSheetUpdateView,
)

urlpatterns = [
    path("", TimeSheetListView.as_view(), name="timesheet-list"),
    path("detail/<int:pk>/", TimeSheetDetailView.as_view(), name="timesheet-detail"),
    path("update/<int:pk>/", TimeSheetUpdateView.as_view(), name="timesheet-update"),
    path("create/", TimeSheetCreateView.as_view(), name="timesheet-create"),
]
