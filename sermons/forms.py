from django import forms
from .models import Sermon
from groups.models import MinistryGroup


class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = [
            "title",
            "preacher",
            "date",
            "scripture",
            "pdf",
            "video_url",
            "thumbnail",
            "group",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter sermon title",
                }
            ),
            "preacher": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                    "placeholder": "select preacher",
                }
            ),  # This is for an existing user
            # "preacher": forms.TextInput(
            #     attrs={
            #         "class": "input input-bordered w-full",
            #         "placeholder": "enter preacher name",
            #     }
            # ),
            "date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter sermon date",
                    "type": "date",
                }
            ),
            "scripture": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter scripture",
                }
            ),
            "pdf": forms.FileInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "upload pdf",
                }
            ),
            "video_url": forms.URLInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter video url",
                }
            ),
            "thumbnail": forms.FileInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "upload thumbnail",
                }
            ),
            "group": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                    "placeholder": "select group",
                }
            ),
        }
