from django import forms

from .models import Address, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "is_whatsapp", "whatsapp", "profile")


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
