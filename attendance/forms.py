from django import forms
from .models import AttendanceSheet, AttendanceRecord
from groups.models import MinistryGroup
from django.contrib.auth.models import User
from events.models import Event
from sermons.models import Sermon


class AttendanceSheetForm(forms.ModelForm):
    class Meta:
        model = AttendanceSheet
        fields = ["date", "type", "group", "sermon", "event"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter date",
                    "type": "date",
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                    "placeholder": "select attendance type",
                }
            ),
            "group": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                    "placeholder": "select group",
                }
            ),
            "sermon": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                    "placeholder": "select group",
                }
            ),
            "event": forms.Select(
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


class AttendanceFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "input input-bordered"}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "input input-borderd"}),
    )
    type = forms.ChoiceField(
        required=False,
        choices=[("", "All types")] + list(AttendanceSheet.ATTENDANCE_TYPES),
        widget=forms.Select(attrs={"class": "select select-bordered"}),
    )

    group = forms.ModelChoiceField(
        required=False,
        queryset=MinistryGroup.objects.all(),
        widget=forms.Select(attrs={"class": "select select-bordered"}),
    )

    sermon = forms.ModelChoiceField(
        required=False,
        queryset=Sermon.objects.all(),
        widget=forms.Select(attrs={"class": "select select-bordered"}),
    )

    event = forms.ModelChoiceField(
        required=False,
        queryset=Event.objects.all(),
        widget=forms.Select(attrs={"class": "select select-bordered"}),
    )
