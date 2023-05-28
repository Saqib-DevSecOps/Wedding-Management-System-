from django.urls import path

from .views import ProviderJsonView

app_name = 'admins-json'

urlpatterns = [
    path('provider', ProviderJsonView.as_view(), name='provider-json-api')
]
