from django import forms
from .models import MinistryGroup


class MinistryGroupForm(forms.ModelForm):
    class Meta:
        model = MinistryGroup
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "enter group name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "enter group description",
                }
            ),
        }
