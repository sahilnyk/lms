from rest_framework import permissions

class IsTenantUser(permissions.BasePermission):
    """
    Allows access only to users belonging to the requested tenant (organisation).
    Checks organisation_id in URL kwargs, request.data, or request.query_params.
    """
    def has_permission(self, request, view):
        org_id = None
        # Try to get organisation_id from URL kwargs
        if hasattr(view, 'kwargs') and view.kwargs:
            org_id = view.kwargs.get('organisation_id')
        # If not found, try request.data (for POST, PUT, PATCH)
        if not org_id:
            org_id = request.data.get('organisation_id') if hasattr(request, 'data') else None
        # If still not found, try query params (for GET)
        if not org_id:
            org_id = request.query_params.get('organisation_id') if hasattr(request, 'query_params') else None
        user = request.user
        # Only allow if user is authenticated and belongs to the requested organisation
        if not user or not user.is_authenticated or not org_id:
            return False
        # Compare user's organisation id with the requested org_id
        return str(getattr(user, 'organisation_id', None)) == str(org_id)