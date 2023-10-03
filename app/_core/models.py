from datetime import datetime, time, timedelta
from decimal import Decimal

from django.db import models
from django.shortcuts import reverse


class Department(models.Model):
    """
    Department model
    """

    name = models.CharField(max_length=255)
    supervisor = models.CharField(max_length=255)
    supervisor_email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


class Role(models.Model):
    """
    Role model
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dept = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="roles")

    def __str__(self):
        return self.name


class TimeSheet(models.Model):
    """
    TimeSheet model
    """
    date = models.DateField()
    name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="timesheets")
    description = models.TextField(blank=True, null=True)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    hours = models.DecimalField(
        max_digits=10, decimal_places=1, default=0, null=True, blank=True
    )
    primary_hours = models.DecimalField(
        max_digits=10, decimal_places=1, default=0, null=True, blank=True
    )
    secondary_hours = models.DecimalField(
        max_digits=10, decimal_places=1, default=0, null=True, blank=True
    )
    primary_overtime = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0
    )
    secondary_overtime = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0
    )
    overtime = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0
    )

    class Meta:
        ordering = ["date"]

    def get_absolute_url(self):
        return reverse("timesheet-detail", kwargs={"pk": self.pk})

    def get_hourly_rate(self):
        return (self.salary * 12) / 1950

    def save(self, *args, **kwargs):
        # Calculate the duration
        duration = self.end_date_time - self.start_date_time

        # Get hourly rate
        self.hourly_rate = self.get_hourly_rate()

        # Get overtime
        hours_worked = Decimal(duration.total_seconds() / 3600)
        self.hours = round(hours_worked, 1)
        if self.date.weekday() < 5:
            if 0 < self.hours < 7.5:
                self.overtime = self.hourly_rate * self.hours * Decimal(1.5)
                self.primary_hours = self.hours
                self.primary_overtime = self.overtime
                self.secondary_hours = 0
                self.secondary_overtime = 0
            elif self.hours > 7.5:
                self.primary_hours = Decimal(7.5)
                self.primary_overtime = (
                    self.hourly_rate * self.primary_hours * Decimal(1.5)
                )
                self.secondary_hours = self.hours - self.primary_hours
                self.secondary_overtime = (
                    self.secondary_hours * self.hourly_rate * Decimal(2.5)
                )
                self.overtime = self.primary_overtime + self.secondary_overtime

        super(TimeSheet, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
