from rest_framework import permissions
from tenancy.models import Organisation


class IsTenantUser(permissions.BasePermission):
    """
    Allows access only to users belonging to the requested tenant (organisation).
    Checks organisation_id in URL kwargs, request.data, or request.query_params.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        org_id = (
            view.kwargs.get('organisation_id') or
            request.data.get('organisation_id') or
            request.query_params.get('organisation_id')
        )
        if not org_id:
            return False
        return str(getattr(user, 'organisation_id', None)) == str(org_id)


class AllowTokenObtain(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return False
        slug = request.data.get('organisation_slug')
        if not slug:
            return False
        return Organisation.objects.filter(slug=slug, status='ACTIVE').exists()