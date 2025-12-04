from django import forms
from .models import Event
from groups.models import MinistryGroup


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "event_type",
            "date",
            "start_time",
            "end_time",
            "location",
            "banner",
            "group",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter event title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "enter event description",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter event date",
                    "type": "date",
                }
            ),
            "start_time": forms.TimeInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter event start time",
                    "type": "time",
                }
            ),
            "end_time": forms.TimeInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter event end time",
                    "type": "time",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter event location",
                }
            ),
            "group": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "event_type": forms.Select(
                attrs={"class": "select select-bordered w-full"}
            ),
            "banner": forms.FileInput(
                attrs={"class": "file-input file-input-bordered w-full"}
            ),
        }
