from rest_framework import permissions


class CanManageListings(permissions.BasePermission):
    """Allow approved providers to manage only their own listings."""

    message = "An approved landlord or agent account is required to manage listings."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.can_manage_listings)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff
                or obj.created_by_id == getattr(request.user, "id", None)
            )
        )


class IsApprovedProvider(permissions.BasePermission):
    """Require a staff member or an approved provider account."""

    message = "An approved landlord or agent account is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.can_manage_listings
        )


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
