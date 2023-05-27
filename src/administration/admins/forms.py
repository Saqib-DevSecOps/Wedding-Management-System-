from django import forms

from .models import GuestGroup, Guest


class GuestGroupMetaForm(forms.ModelForm):
    class Meta:
        model = GuestGroup
        fields = ('group_name',)
        widgets = {
            'group_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class GuestMetaForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ('guest_name',)
        widgets = {
            'guest_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }





