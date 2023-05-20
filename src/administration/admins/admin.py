from django.contrib import admin
from .models import GuestList, GuestGroup, Guest, InvitationLetter, Invitation, Provider, Table, GuestTable


@admin.register(GuestList)
class GuestListAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'user')
    list_filter = ('user',)
    search_fields = ('group_name',)


@admin.register(GuestGroup)
class GuestGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'guest_list')
    list_filter = ('guest_list',)
    search_fields = ('group_name',)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'group')
    list_filter = ('group',)
    search_fields = ('guest_name',)


@admin.register(InvitationLetter)
class InvitationLetterAdmin(admin.ModelAdmin):
    list_display = ('group', 'letter_count')
    list_filter = ('group',)
    search_fields = ('group__group_name',)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('group', 'invitation_count')
    list_filter = ('group',)
    search_fields = ('group__group_name',)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'service', 'email', 'phone_number', 'total_cost', 'paid', 'user')
    list_filter = ('user',)
    search_fields = ('provider_name', 'service', 'email')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'table_type', 'seat_count', 'seats_left', 'user')
    list_filter = ('user',)
    search_fields = ('table_name', 'table_type')


@admin.register(GuestTable)
class GuestTableAdmin(admin.ModelAdmin):
    list_display = ('table', 'guest')
    list_filter = ('table', 'guest')
    search_fields = ('guest__guest_name',)


