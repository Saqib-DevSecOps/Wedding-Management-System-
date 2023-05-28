from crispy_forms.utils import render_crispy_form
from django.shortcuts import get_object_or_404
from django.template.context_processors import csrf
from django.views import View

from src.administration.admins.forms import ProviderMetaForm
from src.administration.admins.models import Provider


class ProviderJsonView(View):

    def post(self, request,  *args, **kwargs):
        form = ProviderMetaForm(data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return {'success': True}

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}
