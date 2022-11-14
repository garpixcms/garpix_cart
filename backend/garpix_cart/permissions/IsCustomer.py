from garpix_user.models import UserSession
from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        customer = UserSession.get_from_request(request=request)
        return customer is not None
