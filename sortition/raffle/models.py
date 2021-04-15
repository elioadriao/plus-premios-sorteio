from django.db import models

from account.models import User

import os


def get_upload_to(instance, filename):
    return os.path.join(
        "rifa",
        "%s_" % str(instance.date.strftime("%m/%d/%Y_%H:%M:%S")), filename
    )


class Raffle(models.Model):
    class Meta:
        verbose_name = "Rifa"
        verbose_name_plural = "Rifas"

    quotas = models.IntegerField(
        verbose_name="Número de Cotas",
        default=1000
    )
    date = models.DateTimeField(
        verbose_name="Data do Sorteio"
    )
    winner = models.IntegerField(
        verbose_name="Vencedor",
        default=0
    )
    image = models.ImageField(
        upload_to=get_upload_to,
        verbose_name="Imagem de Perfil",
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Criador",
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now=True
    )

    def __str__(self):
        return "Data: %s Cotas: %s" % (self.date.strftime("%d/%m/%y %H:%M"), str(self.quotas))


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

    def __str__(self):
        return "Dono: %s Numero: %s" % (self.owner, str(self.number))
