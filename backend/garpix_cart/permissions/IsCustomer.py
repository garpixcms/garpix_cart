from rest_framework import permissions
from ..models import Customer


class IsCustomer(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        customer = Customer.get_from_request(request=request)
        return customer is not None
