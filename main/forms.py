from django import forms
from django.forms import BooleanField

from main.models import Client, Mailing, Notification, Attempt


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs["class"] = "form-control"


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('owner', 'is_active',)

class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)

class NotificationForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Notification
        exclude = ('owner',)

class MailingActivationForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("is_active",)