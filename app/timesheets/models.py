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
        if self.start_date_time.weekday() < 5:
            if 0 < self.get_hours() < 7.5:
                overtime = (
                    self.user.profile.get_hourly_rate()
                    * self.get_hours()
                    * Decimal(1.5)
                )
                # primary_hours = self.hours
                return round(overtime, 2)
                # self.primary_overtime = self.overtime
                # self.secondary_hours = 0
                # self.secondary_overtime = 0
            elif self.get_hours() > 7.5:
                primary_hours = Decimal(7.5)
                primary_overtime = (
                    self.user.profile.get_hourly_rate() * primary_hours * Decimal(1.5)
                )
                secondary_hours = self.get_hours() - primary_hours
                secondary_overtime = (
                    secondary_hours * self.user.profile.get_hourly_rate() * Decimal(2.5)
                )
                overtime = primary_overtime + secondary_overtime
                return round(overtime, 2)

    def __str__(self):
        return f"{self.uid}"