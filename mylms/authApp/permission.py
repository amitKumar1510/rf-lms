from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsPrincipal(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'principal'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'parent'


def is_role_change_allowed(current_user, new_role):
    allowed_map = {
        'admin': ['admin','teacher', 'principal', 'parent'],
        'principal': ['teacher', 'parent', 'student'],
        'teacher': ['student', 'parent'],
    }
    return new_role in allowed_map.get(current_user.role, [])
