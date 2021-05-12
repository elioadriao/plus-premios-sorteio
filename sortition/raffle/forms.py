from django import forms

from .models import Raffle, Quota


class RaffleForm(forms.ModelForm):
    class Meta:
        model = Raffle
        fields = ("title", "description", "quotas", "quota_value", "date", "image")


class QuotaForm(forms.ModelForm):
    class Meta:
        model = Quota
        fields = ("number", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["number"].widget = forms.HiddenInput()
