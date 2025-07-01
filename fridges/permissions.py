from rest_framework import permissions

class IsFridgeProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.fridge.user == request.user