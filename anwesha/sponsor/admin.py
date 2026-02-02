from django.contrib import admin
from .models import Sponsors, MyntraRegistration
from utility import export_as_csv
from django.utils.html import format_html
from django.urls import reverse
from django.db import connection


@admin.register(MyntraRegistration)
class MyntraRegistrationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Myntra Registrations.
    """
    list_display = ('email', 'anwesha_user_id', 'registered_at', 'user_link')
    search_fields = ('email', 'anwesha_user_id')
    readonly_fields = ('registered_at', 'last_synced', 'raw_data')
    list_filter = ('registered_at', 'last_synced')
    actions = ['manual_sync']
    
    def user_link(self, obj):
        """Display link to User if exists"""
        if obj.anwesha_user:
            user = obj.anwesha_user
            url = reverse('admin:user_user_change', args=[user.pk])
            return format_html('<a href="{}">{}</a>', url, user.anwesha_id)
        return "No User"
    user_link.short_description = "User"
    
    def manual_sync(self, request, queryset):
        """Manual sync action - sync_myntra management command does this"""
        self.message_user(request, "Use 'python manage.py sync_myntra' to sync from Google Sheets")
    manual_sync.short_description = "Sync selected from Google Sheets"

@admin.register(Sponsors)
class SponsorsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Sponsors model.
    """

    # Custom action
    actions = [export_as_csv]

    # Displayed fields in the list view
    list_display = (
        'sponsor_name',
        'sponsor_phone_number',
        'sponsor_email',
    )

    # Filtering options in the list view
    list_filter = ()

    # Fieldsets to organize fields in the detail view
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'sponsor_name',
                'sponsor_description',
                'sponsor_phone_number',
                'sponsor_email',
                'sponsor_logo',
                'order',
            )
        }),
        ('Social Links', {
            'fields': (
                ('sponsor_link', 'sponsor_instagram_id'),
                ('sponsor_facebook_id', 'sponsor_linkdin_id')
            )
        }),
    )

    # Displayed value for empty fields
    empty_value_display = '-empty-'

    # Fields to search in the admin interface
    search_fields = [
        'sponsor_name',
        'sponsor_phone_number',
        'sponsor_email',
    ]
