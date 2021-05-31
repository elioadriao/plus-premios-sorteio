from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

import os


def get_upload_to(instance, filename):
    return os.path.join(
        "perfil",
        "%s_" % str(instance.phone), filename
    )


class Address(models.Model):
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    street = models.CharField(
        verbose_name="Rua",
        max_length=255
    )
    number = models.CharField(
        verbose_name="Número",
        max_length=8
    )
    neighborhood = models.CharField(
        verbose_name="Bairro",
        max_length=255
    )
    city = models.CharField(
        verbose_name="Cidade",
        max_length=255
    )
    uf = models.CharField(
        verbose_name="UF",
        max_length=2
    )
    cep = models.CharField(
        verbose_name="CEP",
        max_length=9
    )

    def __str__(self):
        return f"{self.street}, {self.number}, {self.neighborhood}, {self.cep}. {self.city} - {self.uf}."


class UserManager(BaseUserManager):
    def _create_user(self, password=None, **fields):
        user = self.model(**fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **fields):
        return self._create_user(**fields)

    def create_superuser(self, **fields):
        user = self._create_user(is_superuser=True, **fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'whatsapp'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    name = models.CharField(
        verbose_name="Nome",
        max_length=255,
    )
    whatsapp = models.CharField(
        verbose_name="Whatsapp",
        max_length=11,
        unique=True
    )
    email = models.CharField(
        verbose_name="Email",
        max_length=255,
        blank=True,
        null=True
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        verbose_name="Endereço",
        blank=True,
        null=True
    )
    profile = models.ImageField(
        upload_to=get_upload_to,
        verbose_name="Imagem de Perfil",
        blank=True,
        null=True
    )
    is_superuser = models.BooleanField(
        verbose_name="Administrador",
        default=False,
    )
    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now=True
    )

    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    @property
    def is_staff(self):
        return self.is_superuser

    def get_short_name(self):
        return self.name.split(' ')[0]

    def get_full_name(self):
        return self.name
