from django import forms

from .models import Raffle, Quota

from django.core.exceptions import ValidationError


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


class WinnerForm(forms.Form):
    raffle_id = forms.CharField(required=False)
    winner_quota_id = forms.CharField(required=False)
    sorted_quota = forms.CharField(required=False)

    def clean(self):
        data = self.cleaned_data
        sorted_quota = data["sorted_quota"]
        raffle_id = data["raffle_id"]
        try:
            quota = Quota.objects.get(raffle_id=raffle_id, number=sorted_quota)
            if quota.owner:
                if quota.status == "paid":
                    data["winner_quota_id"] = quota.id
                else:
                    raise ValidationError("Cota não possui pagamento registrado.")
            else:
                raise ValidationError("Cota não possui usuário registrado.")
        except Quota.DoesNotExist:
            raise ValidationError("Cota não cadastrada!")

        return data
