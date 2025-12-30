from django.contrib import admin
from .models import Organisation

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "status", "subscription_status", "created_at")
    search_fields = ("name", "slug")
    list_filter = ("status", "subscription_status")

admin.site.register(Organisation, OrganisationAdmin)
