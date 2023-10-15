import uuid
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL


class OvertimeRate(models.Model):
    """
    Overtime Rate model
    """

    name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return self.name


class TimeSheet(models.Model):
    """
    TimeSheet model
    """

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_timesheets"
    )
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_holiday = models.BooleanField(default=False)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("timesheet-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.uid)
        super(TimeSheet, self).save(*args, **kwargs)

    def get_hours(self):
        duration = self.end_date_time - self.start_date_time
        hours_worked = round(Decimal(duration.total_seconds() / 3600), 1)
        return hours_worked

    def get_overtime(self):
        hours = self.get_hours()
        hourly_rate = self.user.profile.get_hourly_rate()

        if self.start_date_time.weekday() < 5 and self.is_holiday == False:
            print("weekday")
            if hours <= 7.5:
                overtime = hourly_rate * hours * Decimal(1.5)
            else:
                primary_hours = Decimal(7.5)
                primary_overtime = hourly_rate * primary_hours * Decimal(1.5)
                secondary_hours = hours - primary_hours
                secondary_overtime = secondary_hours * hourly_rate * Decimal(2.5)
                overtime = primary_overtime + secondary_overtime
        elif self.start_date_time.weekday() == 5 and self.is_holiday == False:
            print("saturday")
            if hours <= 4:
                overtime = hourly_rate * hours * Decimal(1.5)
            elif hours <= 8:
                primary_hours = Decimal(4)
                primary_overtime = hourly_rate * primary_hours * Decimal(1.5)
                secondary_hours = hours - primary_hours
                secondary_overtime = secondary_hours * hourly_rate * Decimal(2)
                overtime = primary_overtime + secondary_overtime
            else:
                primary_hours = Decimal(4)
                secondary_hours = Decimal(8)
                primary_overtime = hourly_rate * primary_hours * Decimal(1.5)
                secondary_overtime = hourly_rate * secondary_hours * Decimal(2)
                tertiary_hours = hours - (primary_hours + secondary_hours)
                tertiary_overtime = tertiary_hours * hourly_rate * Decimal(3)
                overtime = primary_overtime + secondary_overtime + tertiary_overtime
        elif self.is_holiday:
            print("holiday")
            if hours <= 8:
                overtime = hourly_rate * hours * Decimal(2)
            else:
                primary_hours = Decimal(8)
                primary_overtime = hourly_rate * primary_hours * Decimal(2)
                secondary_hours = hours - primary_hours
                secondary_overtime = secondary_hours * hourly_rate * Decimal(3)
                overtime = primary_overtime + secondary_overtime
        elif self.start_date_time.weekday() == 6:
            print("sunday")
            if hours <= 8:
                overtime = hourly_rate * hours * Decimal(2)
            else:
                primary_hours = Decimal(8)
                primary_overtime = hourly_rate * primary_hours * Decimal(2)
                secondary_hours = hours - primary_hours
                secondary_overtime = secondary_hours * hourly_rate * Decimal(3)
                overtime = primary_overtime + secondary_overtime

        return round(overtime, 2)

    def __str__(self):
        return f"{self.uid}"
