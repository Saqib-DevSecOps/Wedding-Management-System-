from django.contrib import admin
from .models import GuestGroup, Guest, InvitationLetter, Provider, Table, GuestTable, EventTimeLine


class GuestInline(admin.TabularInline):
    model = Guest
    extra = 1


@admin.register(GuestGroup)
class GuestGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name','sequence', 'user', 'created_at', 'updated_at')
    inlines = [GuestInline]
    list_filter = ('user',)
    search_fields = ('group_name', 'user__username')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'group', 'created_at', 'updated_at')
    list_filter = ('group__group_name',)
    search_fields = ('guest_name', 'group__group_name')


@admin.register(InvitationLetter)
class InvitationLetterAdmin(admin.ModelAdmin):
    list_display = ('group', 'total_invitation', 'created_at', 'updated_at')
    list_filter = ('group__group_name',)
    search_fields = ('group__group_name',)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider_name', 'service', 'email', 'phone_number', 'total_cost', 'paid', 'comment')
    list_filter = ('user', 'service')
    search_fields = ('provider_name', 'service', 'email', 'user__username')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('user', 'table_name', 'table_type', 'seat_count', 'seats_left')
    list_filter = ('user', 'table_type')
    search_fields = ('table_name', 'user__username')


@admin.register(GuestTable)
class GuestTableAdmin(admin.ModelAdmin):
    list_display = ('table', 'guest')
    list_filter = ('table__table_name',)
    search_fields = ('guest__guest_name', 'table__table_name')


@admin.register(EventTimeLine)
class GuestTableAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('user',)
    search_fields = ('user', 'title')
