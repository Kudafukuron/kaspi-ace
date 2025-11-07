from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    # Access only for owner, manager
    def has_permission(self, request, view):
        role = getattr(request.user, "role", None)
        return request.user.is_authenticated and role in ["owner", "manager"]
    
class IsOwnerOrManager(BasePermission):
    # Manager and owner access
    def has_permission(self, request, view):
        role = getattr(request.user, "role", None)
        return request.user.is_authenticated and role in ["owner", "manager"]
    
    # Allow access for only owner
    #def has_permission(self, request, view):
    #    return request.user.is_authenticated and getattr(request.user, "role", None) == "owner"
