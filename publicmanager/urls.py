"""publicmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls import path, include, re_path

admin.site.site_header = "1GOV"
admin.site.index_title = "1GOV"
admin.site.site_title = 'Admin'

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('publicmanager.autenticacao.urls', namespace='autenticacao')),
    path('painel/', include('publicmanager.dashboard.urls', namespace='dashboard')),
    
    # Saúde
    path('saude/', include('publicmanager.saude.urls', namespace='saude')),
    path('cadastro/', include('publicmanager.saude_cadastro.urls', namespace='saude_cadastro')),
    path('farmacia/', include('publicmanager.saude_farmacia.urls', namespace='saude_farmacia')),
    path('atendimento/', include('publicmanager.saude_atendimento.urls', namespace='saude_atendimento')),
    path('enfermagem/', include('publicmanager.saude_enfermagem.urls', namespace='saude_enfermagem')),
    path('financeiro/', include('publicmanager.saude_financeiro.urls', namespace='saude_financeiro')),

    # Outros Modulos Adicionais
    path('comum/', include('publicmanager.comum.urls', namespace='comum')),
    path('chaining/', include('smart_selects.urls')),
    path('rh/', include('publicmanager.rh.urls', namespace='rh')),
    path('agricultura/', include('publicmanager.agricultura.urls', namespace='agricultura')),

    path('sentry-debug/', trigger_error),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]