from rest_framework import permissions

class IsSupportAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'support_team_member') and request.user.support_team_member.is_admin

class IsSupportTeamMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'support_team_member')
