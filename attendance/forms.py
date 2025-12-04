from django import forms
from .models import Attendance, AttendanceRecord
from groups.models import MinistryGroup
from django.contrib.auth.models import User


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["date", "group"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter date",
                    "type": "date",
                }
            ),
            "group": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                    "placeholder": "select group",
                }
            ),
        }


class MarkAttendanceForm(forms.Form):
    """Dynamic checkbox form for marking attndance"""

    def __init__(self, users, initial_present, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for user in users:
            self.fields[f"user_{user.id}"] = forms.BooleanField(
                required=False,
                initial=user.id in initial_present,
                label=user.username,
            )
