import csv
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import TimeSheetCreateForm, TimeSheetUpdateForm
from .models import TimeSheet


class TimeSheetListView(ListView):
    model = TimeSheet


class TimeSheetDetailView(DetailView):
    model = TimeSheet


def create_time_sheet(request):
    form = TimeSheetCreateForm(request.POST or None)

    if form.is_valid():
        # hours = round(hours_worked, 1)

        # Now 'created' contains the value of the 'created' field from the form

        # Do something with the value, for example, print it
        # print(created)

        # If you want to save the form, you can do it like this:
        time_sheet = form.save(commit=False)
        time_sheet.user = request.user
        time_sheet.save()
        return redirect("/")

    return render(request, "timesheets/create_timesheet.html", {"form": form})


def export_to_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="timesheets.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["User", "Start Date Time", "End Date Time", "Description"]
    )  # Write header row

    timesheets = TimeSheet.objects.all()
    for timesheet in timesheets:
        writer.writerow(
            [
                timesheet.user.username,
                timesheet.start_date_time,
                timesheet.end_date_time,
                timesheet.description,
            ]
        )

    return response


# Create your views here.
# hours_worked = Decimal(duration.total_seconds() / 3600)
#         self.hours = round(hours_worked, 1)
#         if self.date.weekday() < 5:
#             if 0 < self.hours < 7.5:
#                 self.overtime = self.hourly_rate * self.hours * Decimal(1.5)
#                 self.primary_hours = self.hours
#                 self.primary_overtime = self.overtime
#                 self.secondary_hours = 0
#                 self.secondary_overtime = 0
#             elif self.hours > 7.5:
#                 self.primary_hours = Decimal(7.5)
#                 self.primary_overtime = (
#                     self.hourly_rate * self.primary_hours * Decimal(1.5)
#                 )
#                 self.secondary_hours = self.hours - self.primary_hours
#                 self.secondary_overtime = (
#                     self.secondary_hours * self.hourly_rate * Decimal(2.5)
#                 )
#                 self.overtime = self.primary_overtime + self.secondary_overtime

#   def save(self, *args, **kwargs):
#         # Calculate the duration
#         duration = self.end_date_time - self.start_date_time

#         # Get overtime

#         super(TimeSheet, self).save(*args, **kwargs)
