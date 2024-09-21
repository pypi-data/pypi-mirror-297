from django.contrib import messages
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from zero_theme.generics.models import thread_local


class ZeroMiddleware(MiddlewareMixin):
    """
     Middleware to store the current user in thread-local storage.
     """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_local.user = request.user
        response = self.get_response(request)
        return response

    def process_response(self, request, response):
        if request.path.__contains__(reverse('admin:password_change_done')):
            response = redirect(reverse('admin:index'))
            messages.add_message(request, messages.SUCCESS, _('Your password has been successfully changed.'))

        if request.path.__contains__(reverse('admin:logout')):
            response = redirect(reverse('admin:index'))
        return response
