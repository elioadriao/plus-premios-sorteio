from django import forms

from .models import Raffle, Quota

from django.core.exceptions import ValidationError


class RaffleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RaffleForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Raffle
        fields = ("title", "owner", "description", "quotas", "quota_value", "date", "image")


class RaffleFilterForm(forms.Form):
    FILTER_CHOICES = [("all", "Todos"), ("open", "Disponiveis"), ("closed", "Finalizados")]
    status = forms.ChoiceField(choices=FILTER_CHOICES, widget=forms.RadioSelect())


class QuotaForm(forms.Form):
    quotas = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, required=True, queryset=Quota.objects.none()
    )

    def __init__(self, *args, **kwargs):
        raffle_pk = kwargs.pop("raffle_pk", None)
        super().__init__(*args, **kwargs)
        self.fields["quotas"].queryset = Quota.objects.filter(order__isnull=True, raffle_id=raffle_pk)


class WinnerForm(forms.Form):
    winner_quota_id = forms.CharField(required=False)
    sorted_quota = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.raffle_pk = kwargs.pop("raffle_pk", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        sorted_quota = data["sorted_quota"]
        try:
            quota = Quota.objects.get(raffle_id=self.raffle_pk, number=sorted_quota)
            if quota.order:
                if quota.order.status == "paid":
                    data["winner_quota_id"] = quota.id
                else:
                    raise ValidationError("Cota não possui pagamento registrado.")
            else:
                raise ValidationError("Cota não possui usuário registrado.")
        except Quota.DoesNotExist:
            raise ValidationError("Cota não cadastrada!")

        return data
