import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class User(AbstractUser):
    is_developer = models.BooleanField(default=False)
    is_admin_manager = models.BooleanField(default=True)
    is_supervisor = models.BooleanField(default=False)


class Department(models.Model):
    """
    Department model
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    supervisor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="supervisor"
    )

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


class Gender(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    slug = models.SlugField(max_length=255, blank=True)
    gender = models.ForeignKey(
        Gender,
        on_delete=models.PROTECT,
        related_name="gender_list",
        null=True,
        blank=True,
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="role_list",
        null=True,
        blank=True,
    )
    phone = models.CharField(max_length=20, null=True, default="+1")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.uid)
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"slug": self.slug})

    def get_hourly_rate(self):
        return round(((self.salary * 12) / 1950), 2)

    def get_profile_initials(self):
        if self.name:
            return f"{self.name[0]}"

    def __str__(self) -> str:
        if self.name:
            return f"{self.name}"
        return self.user.email
