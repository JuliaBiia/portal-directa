from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TipoProdutorForm
from .models import TipoProdutor


class TipoProdutorListView(LoginRequiredMixin, ListView):
    model = TipoProdutor
    context_object_name = 'tipoprodutores'
    template_name = 'tipoprodutor.html'

class TipoProdutorCreateView(LoginRequiredMixin, CreateView):
    model = TipoProdutor
    template_name = 'tipoprodutor_create_update_form.html'
    form_class = TipoProdutorForm
    success_url = '/agricultura/tipoprodutor/'


class TipoProdutorUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoProdutor
    template_name = 'tipoprodutor_create_update_form.html'
    form_class = TipoProdutorForm
    success_url = '/agricultura/tipoprodutor/'


class TipoProdutorDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoProdutor
    template_name = "tipoprodutor.html"
    success_url = '/agricultura/tipoprodutor/'
