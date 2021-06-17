from django.db import models

from django.utils import timezone

from django.conf import settings

from ..account.models import User

import os


def get_upload_to(instance, filename):
    return os.path.join(
        "rifas",
        "%s.%s" % (timezone.now().strftime("%s"), filename.split(".")[-1])
    )


class Raffle(models.Model):
    class Meta:
        verbose_name = "Rifa"
        verbose_name_plural = "Rifas"

    title = models.CharField(
        verbose_name="Titulo do Sorteio",
        max_length=255,
        null=True
    )
    description = models.CharField(
        verbose_name="Descrição do Sorteio",
        max_length=255,
        null=True,
        blank=True
    )
    quotas = models.IntegerField(
        verbose_name="Número de Cotas",
        default=100
    )
    quota_value = models.CharField(
        verbose_name="Valor Unitário da Cota",
        max_length=10,
        default="R$ 100,00"
    )
    date = models.DateTimeField(
        verbose_name="Data do Sorteio",
        null=True,
        blank=True
    )
    owner = models.CharField(
        verbose_name="Dono Titular",
        max_length=255,
        null=True,
        blank=True
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Vencedor",
        related_name="winner_set",
        null=True,
        blank=True
    )
    sorted_quota = models.IntegerField(
        verbose_name="Cota Sorteada",
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to=get_upload_to,
        verbose_name="Imagem Ilustrativa do Sorteio",
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Criador",
        related_name="created_by_set",
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True
    )

    def __str__(self):
        return "ID: %s Cotas: %s" % (str(self.id), str(self.quotas))

    def is_buy_valid(self):
        if self.date:
            return self.date > timezone.now()
        else:
            if self.get_paid_percent() == 100:
                return False
            else:
                return True

    def get_date(self):
        if self.date:
            return "%s ás %s" % (self.date.strftime("%d/%m/%y"), self.date.strftime("%H:%M"))
        else:
            return "Ao final de venda de todas as Cotas"

    def is_sorted(self):
        return (self.winner and self.sorted_quota)

    def get_quota_value(self):
        return int(self.quota_value.split(",")[0][3:])

    def dump_orders(self):
        for order in QuotaOrder.objects.all():
            if order.get_raffle().id == self.id:
                order.delete()
        self.quota_set.all().delete()

    def get_open_percent(self):
        open_quotas_count = self.quota_set.filter(order__isnull=True).count()
        return int((open_quotas_count * 100) / self.quotas)

    def get_reserved_percent(self):
        reserved_quotas_count = self.quota_set.filter(order__status="reserved").count()
        return int((reserved_quotas_count * 100) / self.quotas)

    def get_paid_percent(self):
        paid_quotas_count = self.quota_set.filter(order__status="paid").count()
        return int((paid_quotas_count * 100) / self.quotas)


class QuotaOrder(models.Model):
    class Meta:
        verbose_name = "Reserva de Cota"
        verbose_name_plural = "Reservas de Cotas"

    ORDER_STATUS = [
        ("reserved", "Reservado"),
        ("paid", "Pago")
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Dono",
        null=True
    )
    value = models.CharField(
        verbose_name="Valor da Reserva",
        max_length=10,
        default="R$ 100,00"
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=8,
        choices=ORDER_STATUS,
        default="reserved"
    )
    reserved_at = models.DateTimeField(
        verbose_name="Reservado em",
        auto_now_add=True
    )
    paid_at = models.DateTimeField(
        verbose_name="Pago em",
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s Valor: %s" % (self.get_status(), self.value)

    def get_status(self):
        return dict(self.ORDER_STATUS).get(self.status)

    def get_quotas_numbers(self):
        return ", ".join(map(str, self.quota_set.all().values_list("number", flat=True)[::1]))

    def get_raffle(self):
        return self.quota_set.first().raffle

    def get_payment_link(self):
        return settings.WHATSAPP_LINK.format(self.value)


class Quota(models.Model):
    class Meta:
        verbose_name = "Cota"
        verbose_name_plural = "Cotas"

    raffle = models.ForeignKey(
        Raffle,
        on_delete=models.CASCADE,
        verbose_name="Rifa",
        null=True
    )
    order = models.ForeignKey(
        QuotaOrder,
        on_delete=models.CASCADE,
        verbose_name="Reserva de Cota",
        blank=True,
        null=True
    )
    number = models.IntegerField(
        verbose_name="Numero",
        default=0
    )

    def __str__(self):
        return str(self.number)

    def get_status(self):
        if self.order:
            return self.order.get_status()
        else:
            return "Aberto"

    def get_btn(self):
        if self.order:
            if self.get_status() == "Reservado":
                return "warning"
            else:
                return "danger"
        else:
            return "success"
