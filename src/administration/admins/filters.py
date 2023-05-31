import django_filters
from crispy_forms.layout import Row, Column, Div
from django.forms import TextInput

from src.accounts.models import User
from src.administration.admins.models import Guest, Provider


class Row(Div):
    css_class = "row"


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'username'}), lookup_expr='icontains')
    first_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'first name'}),
                                           lookup_expr='icontains')
    last_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'last name'}), lookup_expr='icontains')
    email = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'email'}), lookup_expr='icontains')

    class Meta:
        model = User
        fields = {}


class GuestFilter(django_filters.FilterSet):
    guest_name = django_filters.CharFilter(lookup_expr='icontains', label='', widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Guest Name'}))

    class Meta:
        model = Guest
        fields = ['guest_name', 'group']

    def __init__(self, *args, **kwargs):
        super(GuestFilter, self).__init__(*args, **kwargs)
        self.form.fields['group'].widget.attrs.update({"class": "form-control"})
        self.form.fields['group'].empty_label = 'Select Group'


class ProviderFilter(django_filters.FilterSet):
    class Meta:
        model = Provider
        fields = ['provider_name', 'service']

    def __init__(self, *args, **kwargs):
        super(ProviderFilter, self).__init__(*args, **kwargs)
        self.form.fields['provider_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Provider Name'})
        self.form.fields['service'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Service Name'})
