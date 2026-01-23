from rest_framework import permissions

class IsTenantUser(permissions.BasePermission):
    """
    Allows access only to users belonging to the requested tenant (organisation).
    """
    def has_permission(self, request, view):
        # Try to get organisation_id from URL kwargs or request data
        org_id = view.kwargs.get('organisation_id') or request.data.get('organisation_id')
        user = request.user

        # Only allow if user is authenticated and belongs to the requested organisation
        if not user.is_authenticated or not org_id:
            return False

        # Compare user's organisation id with the requested org_id
        return str(user.organisation_id) == org_id