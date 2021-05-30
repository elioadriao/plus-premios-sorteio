from django.db import models

from django.utils import timezone

from datetime import datetime

from ..account.models import User

import os


def get_upload_to(instance, filename):
    return os.path.join(
        "rifas",
        "%s.%s" % (str(datetime.now().timestamp()), filename.split('.')[-1])
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
        verbose_name="Data do Sorteio"
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
        auto_now=True
    )

    def __str__(self):
        return "ID: %s Data: %s Cotas: %s" % (
            str(self.id), self.date.strftime("%d/%m/%y %H:%M"), str(self.quotas)
        )

    def is_date_valid(self):
        return self.date > timezone.now()

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return "static/vendor/img/empty.png"


class Quota(models.Model):
    class Meta:
        verbose_name = "Cota"
        verbose_name_plural = "Cotas"

    QUOTA_STATUS = [
        ("open", "Aberto"),
        ("reserved", "Reservado"),
        ("paid", "Pago")
    ]

    raffle = models.ForeignKey(
        Raffle,
        on_delete=models.CASCADE,
        verbose_name="Rifa",
        null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Dono",
        blank=True,
        null=True
    )
    number = models.IntegerField(
        verbose_name="Numero",
        default=0
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=8,
        choices=QUOTA_STATUS,
        default="open"
    )
    reserved_at = models.DateTimeField(
        verbose_name="Reservado em",
        blank=True,
        null=True
    )
    paid_at = models.DateTimeField(
        verbose_name="Pago em",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Cota %s" % (str(self.number))

    def get_status(self):
        return dict(self.QUOTA_STATUS).get(self.status)

    def get_btn(self):
        if self.status == "open":
            return "success"
        elif self.status == "reserved":
            return "warning"
        else:
            return "primary"
