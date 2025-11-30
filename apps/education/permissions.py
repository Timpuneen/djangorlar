from rest_framework import permissions

class IsCourseOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a course to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'course'):
            return obj.course.owner == request.user
        return False
            
