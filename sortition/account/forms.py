from django import forms

from .models import Address, User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("whatsapp", "name", "email", "profile")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get("whatsapp")
        wpp_cleaned = whatsapp.split(" ")[1]
        if "_" in wpp_cleaned:
            raise forms.ValidationError("Whatsapp invalido ou incorreto.")
        if User.objects.filter(whatsapp__endswith=wpp_cleaned).exists():
            raise forms.ValidationError("Whatsapp já cadastrado no sistema.")
        return whatsapp

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Senha deve ter no minimo 8 digitos.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Os dois campos de senha não coincidem.")
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
