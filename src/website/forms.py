from .models import ContactRequest
from django.forms import ModelForm


class ContactRequestForm(ModelForm):

    class Meta:
        model = ContactRequest
        fields = '__all__'
