from rest_framework import permissions

class IsSupportAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.support_team_member and request.user.support_team_member.is_admin:
            return True
        return False
        return super().has_permission(request, view)