from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import TimeSheetCreateForm, TimeSheetUpdateForm
from .models import TimeSheet


class TimeSheetCreateView(CreateView):
    model = TimeSheet
    form_class = TimeSheetCreateForm


class TimeSheetUpdateView(UpdateView):
    model = TimeSheet
    form_class = TimeSheetUpdateForm

    # def test_func(self):
    #     return self.request.user.email.endswith("@example.com")


class TimeSheetListView(ListView):
    model = TimeSheet


class TimeSheetDetailView(DetailView):
    model = TimeSheet
