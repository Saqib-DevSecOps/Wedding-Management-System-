import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, CreateView
)
from django.views import View
from django.http import JsonResponse
from src.administration.admins.filters import GuestFilter, ProviderFilter
from src.administration.admins.forms import GuestGroupMetaForm, ProviderMetaForm, GuestMetaForm, InvitationForm, \
    TableForm
from src.administration.admins.models import GuestGroup, Guest, Provider, InvitationLetter, GuestTable

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """
    Registrations: Today, Month, Year (PAID/UNPAID)
    Subscriptions: Today, Month, Year (TYPES)
    Withdrawals  : Today, Month, Year (CALCULATE)
    """
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        # context = calculate_statistics(context)
        # initialization(init=False, mid=False, end=False)
        return context


@method_decorator(login_required, name='dispatch')
class GuestGroupListView(CreateView, ListView):
    model = GuestGroup
    form_class = GuestGroupMetaForm
    template_name = 'admins/guest_group_list.html'
    success_url = reverse_lazy("admins:guest-group-list")

    def get_queryset(self):
        search = self.request.GET.get('guest_group_search')
        if search:
            return self.model.objects.filter(user=self.request.user, group_name__icontains=search)
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        guest_names = self.request.POST.getlist('guest_names[]')
        guest_group = form.save(commit=False)  # Get the saved GuestGroup instance
        guest_group.user = self.request.user
        guest_group.save()
        invitation_letter, created = InvitationLetter.objects.get_or_create(group=guest_group)
        invitation_letter.save()
        # Save guest names to the guest group
        for name in guest_names:
            Guest.objects.create(guest_name=name, group=guest_group)
        messages.success(self.request, 'Guest Group Created Successfully')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuestGroupListView, self).get_context_data(**kwargs)
        context['invitation_from'] = InvitationForm
        return context


@method_decorator(login_required, name='dispatch')
class GuestGroupDetailView(DetailView):
    model = GuestGroup
    template_name = 'admins/guest_group_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(GuestGroup, pk=self.kwargs['pk'], user=self.request.user)


@login_required
def update_guest_group(request):
    if request.method == "GET":
        group_id = request.GET.get('group_id')
        guest_group = get_object_or_404(GuestGroup, id=group_id, user=request.user)

        # Prepare the data to be sent in the response
        response_data = {
            'success': True,
            'group_name': guest_group.group_name,
            'guest_names': list(guest_group.guest_set.values_list('guest_name', flat=True)),
        }
        print(response_data)

        return JsonResponse(response_data)
    if request.method == "POST":
        group_id = request.POST.get('group_id')
        group_name = request.POST.get('group_name')
        guest_names = request.POST.getlist('guest_names[]')

        # Fetch the guest group object
        guest_group = get_object_or_404(GuestGroup, id=group_id, user=request.user)

        # Update the guest group data
        guest_group.group_name = group_name
        guest_group.save()

        # Update the guest names
        guest_group.guest_set.all().delete()  # Remove existing guest names
        for name in guest_names:
            guest_group.guest_set.create(guest_name=name)
        messages.success(request, "Group Updated Successfully")
        return JsonResponse({'success': True})


@method_decorator(login_required, name='dispatch')
class GuestGroupUpdateView(UpdateView):
    model = GuestGroup
    form_class = GuestGroupMetaForm
    template_name = 'admins/guest_group_update.html'
    success_url = reverse_lazy('admins:guest-group-list')

    def form_valid(self, form):
        guest_group = form.save()
        # Handle saving the updated guest list if necessary
        return JsonResponse({'success': True})


class InvitationUpdateView(View):

    def get(self, request, pk):
        invitation = get_object_or_404(GuestGroup, id=pk)
        data = {
            'total_invitation': invitation.invitation_set.total_invitation,
        }
        return JsonResponse({'invitation': data})

    def post(self, request, pk):
        invitation = get_object_or_404(GuestGroup, id=pk)
        form = InvitationForm(request.POST, request.FILES, instance=invitation.invitation_set)
        if form.is_valid():
            invitation = form.save()
            messages.success(request, "Successfully updated")
            return JsonResponse({'success': True, 'provider_id': invitation.id})

        errors = {}
        for field, error_messages in form.errors.items():
            print("invalid")

            errors[field] = [str(message) for message in error_messages]

        return JsonResponse({'errors': errors}, status=400)


@method_decorator(login_required, name='dispatch')
class GuestGroupDeleteView(View):
    def get(self, request, pk):
        print("hello")
        guest = get_object_or_404(GuestGroup, pk=pk)
        guest.delete()
        messages.success(self.request, "Provider Successfully Deleted")
        return redirect('admins:guest-group-list')


@method_decorator(login_required, name='dispatch')
class GuestListView(CreateView, ListView):
    model = Guest
    form_class = GuestMetaForm
    template_name = 'admins/guest_list.html'
    success_url = reverse_lazy("admins:guest-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(group__user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GuestListView, self).get_context_data(**kwargs)
        filter_object = GuestFilter(self.request.GET, queryset=self.get_queryset())
        context['object_list'] = filter_object.qs
        context['filter_form'] = filter_object.form
        return context


@method_decorator(login_required, name='dispatch')
class GuestDeleteView(View):
    def get(self, request, pk):
        print("hello")
        guest = get_object_or_404(Guest, id=pk)
        guest.delete()
        messages.success(self.request, "Guest Successfully Deleted")
        return redirect('admins:guest-list')


@require_GET
def get_guests(request):
    group_id = request.GET.get('group_id')
    group = get_object_or_404(GuestGroup, id=group_id)
    guests = Guest.objects.filter(group=group)
    guest_list = [{'name': guest.guest_name} for guest in guests]
    return JsonResponse(guest_list, safe=False)


@method_decorator(login_required, name='dispatch')
class ProviderListCreateView(ListView):
    model = Provider
    template_name = 'admins/provider_list.html'
    success_url = reverse_lazy("admins:guest-group-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProviderListCreateView, self).get_context_data(**kwargs)
        context['form'] = ProviderMetaForm
        filter_object = ProviderFilter(self.request.GET, queryset=self.get_queryset())
        context['object_list'] = filter_object.qs
        context['filter_form'] = filter_object.form
        return context


@method_decorator(login_required, name='dispatch')
class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'admins/provider_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Provider, id=self.kwargs['pk'], user=self.request.user)


class ProviderCreateView(View):
    def post(self, request):
        form = ProviderMetaForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            provider = form.save(commit=False)
            provider.user = request.user
            provider.save()
            messages.success(request, "Successfully Created")
            return JsonResponse({'success': True, 'provider_id': provider.id})

        errors = {}
        for field, error_messages in form.errors.items():
            errors[field] = [str(message) for message in error_messages]

        return JsonResponse({'errors': errors}, status=400)


class ProviderUpdateView(View):

    def get(self, request, pk):
        provider = get_object_or_404(Provider, id=pk, user=self.request.user)
        print()
        provider_data = {
            'provider_name': provider.provider_name,
            'service': provider.service,
            'email': provider.email,
            'phone_number': provider.phone_number,
            'total_cost': provider.total_cost,
            'paid': provider.paid,
            'comment': provider.comment,
            'attachment': str(provider.attachment.url),
        }
        return JsonResponse({'provider': provider_data})

    def post(self, request, pk):
        provider = get_object_or_404(Provider, id=pk, user=self.request.user)
        form = ProviderMetaForm(request.POST, request.FILES, instance=provider)
        if form.is_valid():
            print("valid")
            provider = form.save()
            messages.success(request, "Successfully updated")
            return JsonResponse({'success': True, 'provider_id': provider.id})

        errors = {}
        for field, error_messages in form.errors.items():
            print("invalid")

            errors[field] = [str(message) for message in error_messages]

        return JsonResponse({'errors': errors}, status=400)


@method_decorator(login_required, name='dispatch')
class ProviderDeleteView(View):
    def get(self, request, pk):
        print("hello")
        provider = get_object_or_404(Provider, id=pk)
        provider.delete()
        messages.success(self.request, "Provider Successfully Deleted")
        return redirect('admins:provider-list')


def update_row_order(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        row_id_list = body.get('row_id_list', [])
        sequence_list = body.get('sequence_list', [])
        for index in range(len(row_id_list)):
            group = GuestGroup.objects.get(pk=int(row_id_list[index]))
            group.sequence = index
            group.save()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request method'})


class SeatPlannerListView(ListView):
    model = GuestTable
    template_name = 'admins/seat_planner_list.html'


class SeatPlannerCreateView(TemplateView):
    template_name = 'admins/create_seat_planner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guests'] = Guest.objects.filter(group__user = self.request.user)
        context['form'] = TableForm
        return context
