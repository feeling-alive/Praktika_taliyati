from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")  # Русское сообщение об ошибке
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Client.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Этот телефон уже используется.")  # Русское сообщение об ошибке
        return phone