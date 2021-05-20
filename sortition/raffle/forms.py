from django import forms

from .models import Raffle, Quota


class RaffleForm(forms.ModelForm):
    class Meta:
        model = Raffle
        fields = ("title", "description", "quotas", "quota_value", "date", "image")


class QuotaForm(forms.Form):
    quotas = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, required=True, queryset=Quota.objects.none()
    )

    def __init__(self, *args, **kwargs):
        raffle_pk = kwargs.pop("raffle_pk", None)
        super().__init__(*args, **kwargs)
        self.fields["quotas"].queryset = Quota.objects.filter(status="open", raffle_id=raffle_pk)
