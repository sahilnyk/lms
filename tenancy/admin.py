from django.contrib import admin
from .models import Organisation

class SubscriptionStatusFilter(admin.SimpleListFilter):
    title = 'Subscription Status'
    parameter_name = 'subscription_status'

    def lookups(self, request, model_admin):
        return (
            ('Active', 'Active'),
            ('Suspended', 'Suspended'),
            ('Unknown', 'Unknown'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Active':
            return queryset.filter(status='ACTIVE')
        elif value == 'Suspended':
            return queryset.filter(status='SUSPENDED')
        elif value == 'Unknown':
            return queryset.exclude(status__in=['ACTIVE', 'SUSPENDED'])
        return queryset

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "status", "subscription_status", "created_at")
    search_fields = ("name", "slug")
    list_filter = ("status", SubscriptionStatusFilter)

admin.site.register(Organisation, OrganisationAdmin)
