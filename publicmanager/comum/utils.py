from typing import OrderedDict
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import AccessMixin

from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

class CheckUserTypeMixin(AccessMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            logout(request)
            return redirect('autenticacao:login')
        
        if not request.user.is_authenticated:
            messages.warning(request, "Sua sessão expirou. Faça login novamente.")
            return redirect('autenticacao:login')

        if not hasattr(request.user, 'tipo_usuario') or not request.user.tipo_usuario:
            logout(request)
            messages.error(request, "Usuário não autenticado.")
            return redirect('autenticacao:login')

        return super().dispatch(request, *args, **kwargs)

class CsrfSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
    
class SimpleAPIPagination(pagination.PageNumberPagination):       
    page_size = 20
    page_size_query_param = 'page_size'
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page_size', self.get_page_size(self.request)),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
