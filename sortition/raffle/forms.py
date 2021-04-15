from django import forms

from .models import Raffle


class UserForm(forms.ModelForm):
    class Meta:
        model = Raffle
        fields = ("quotas", "date", "image")
