from django import forms

from .models import TimeSheet


class TimeSheetCreateForm(forms.ModelForm):
    class Meta:
        model = TimeSheet
        fields = "__all__"
        exclude = ("slug", "user")

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_date_time": forms.TimeInput(attrs={"type": "datetime-local"}),
            "end_date_time": forms.TimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class TimeSheetUpdateForm(forms.ModelForm):
    class Meta:
        model = TimeSheet
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_date_time": forms.TimeInput(attrs={"type": "datetime-local"}),
            "end_date_time": forms.TimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }
