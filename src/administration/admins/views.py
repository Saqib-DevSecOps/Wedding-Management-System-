from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)

# from faker_data import initialization
from src.accounts.models import User
from src.administration.admins.filters import UserFilter
from src.administration.admins.forms import GuestGroupMetaForm
from src.administration.admins.models import GuestGroup, Guest

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]


@method_decorator(admin_decorators, name='dispatch')
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


""" USERS """


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admins/user_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user_filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['user_filter_form'] = user_filter.form

        paginator = Paginator(user_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['user_list'] = user_page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        'profile_image', 'first_name', 'last_name',
        'email', 'username', 'phone_number', 'is_active'
    ]
    template_name = 'admins/user_update_form.html'

    def get_success_url(self):
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})


@method_decorator(admin_decorators, name='dispatch')
class UserPasswordResetView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/admin_password_reset.html', {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
        return render(request, 'admins/admin_password_reset.html', {'form': form})


class GuestGroupListView(CreateView, ListView):
    model = GuestGroup
    form_class = GuestGroupMetaForm
    template_name = 'admins/guest_group_list.html'
    success_url = reverse_lazy("admins:guest-group-list")

    def form_valid(self, form):
        guest_names = self.request.POST.getlist('guest_names[]')
        guest_group = form.save(commit=False)  # Get the saved GuestGroup instance
        guest_group.user = self.request.user
        guest_group.save()
        # Save guest names to the guest group
        for name in guest_names:
            Guest.objects.create(guest_name=name, group=guest_group)
        messages.success(self.request, 'Guest Group Created Successfully')
        return super().form_valid(form)


class GuestGroupDetailView(DetailView):
    model = GuestGroup
    template_name = 'admins/guest_group_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(GuestGroup, pk=self.kwargs['pk'])


class GuestGroupUpdateView(UpdateView):
    model = GuestGroup
    form_class = GuestGroupMetaForm
    template_name = 'admins/guest_group_update.html'
    success_url = reverse_lazy('admins:guest-group-list')

    def form_valid(self, form):
        guest_group = form.save()
        # Handle saving the updated guest list if necessary
        return JsonResponse({'success': True})


class ProviderListCreateView(CreateView, ListView):
    model = GuestGroup
    form_class = GuestGroupMetaForm
    template_name = 'admins/guest_group_list.html'
    success_url = reverse_lazy("admins:guest-group-list")
