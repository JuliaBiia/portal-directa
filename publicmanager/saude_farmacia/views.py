import datetime
from uuid import UUID
from dal import autocomplete
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from publicmanager.comum.utils import CheckUserTypeMixin
from publicmanager.saude_cadastro.models import Profissional
from publicmanager.saude_farmacia.models import (
    Medicamento, Farmacia, RequisicaoMaterialFarmacia, Insumo, MedicamentoRequisitado, InsumoRequisitado, EntradaMaterialFarmacia, 
    InsumoEntrada, MedicamentoEntrada, PrincipioAtivo, Produto, ProdutoEntrada, ProdutoRequisitado
)
from publicmanager.saude_farmacia.forms import (
    EntradaMaterialFarmaciaForm, InsumoEntradaForm, MedicamentoEntradaForm, MedicamentoForm, FarmaciaForm, InsumoForm, InsumoRequisitadoForm, 
    MedicamentoRequisitadoForm, ProdutoEntradaForm, ProdutoForm, ProdutoRequisitadoForm, RequisicaoMaterialFarmaciaForm, PrincipioAtivoForm
)
class PrincipioAtivoListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = PrincipioAtivo
    context_object_name = 'principiosativos'
    template_name = 'saude_farmacia/principio_ativo.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome__icontains=self.request.GET.get("nome_filtro"))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['nome_filtro'] = self.request.GET.get('nome_filtro', '')

        context['crumbs'] = [
            {'label': 'Listagem de Princípios Ativos', 'url': reverse('saude_farmacia:principioativo_list')}
        ]

        return context

class PrincipioAtivoCreateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, CreateView):
    model = PrincipioAtivo
    template_name = 'saude_farmacia/principio_ativo_create_update_form.html'
    form_class = PrincipioAtivoForm
    success_url = reverse_lazy('saude_farmacia:principioativo_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Princípios Ativos', 'url': reverse('saude_farmacia:principioativo_list')},
            {'label': 'Cadastro de Princípio Ativo', 'url': reverse('saude_farmacia:principioativo_add')}
        ]

        return context

class PrincipioAtivoUpdateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, UpdateView):
    model = PrincipioAtivo
    template_name = 'saude_farmacia/principio_ativo_create_update_form.html'
    form_class = PrincipioAtivoForm
    success_url = reverse_lazy('saude_farmacia:principioativo_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Princípios Ativos', 'url': reverse('saude_farmacia:principioativo_list')},
            {'label': 'Editar dados do princípio ativo', 'url': reverse('saude_farmacia:principioativo_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class PrincipioAtivoDeleteView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, DeleteView):
    model = PrincipioAtivo
    template_name = "saude_farmacia/principio_ativo.html"
    success_url = reverse_lazy('saude_farmacia:principioativo_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class FarmaciaListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = Farmacia
    context_object_name = 'farmacias'
    template_name = 'saude_farmacia/farmacia.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade).order_by('nome_farmacia')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "farmacia":
            queryset = queryset.filter(nome_farmacia__icontains=self.request.GET.get('buscar_nome'))
      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "farmacia"

        return context

class FarmaciaCreateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, CreateView):
    model = Farmacia
    template_name = 'saude_farmacia/farmacia_create_update_form.html'
    form_class = FarmaciaForm
    success_url = reverse_lazy('saude_farmacia:farmacia_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class FarmaciaUpdateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, UpdateView):
    model = Farmacia
    template_name = 'saude_farmacia/farmacia_create_update_form.html'
    form_class = FarmaciaForm
    success_url = reverse_lazy('saude_farmacia:farmacia_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class FarmaciaDeleteView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, DeleteView):
    model = Farmacia
    template_name = "saude_farmacia/farmacia.html"
    success_url = reverse_lazy('saude_farmacia:farmacia_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class ProdutoListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = Produto
    context_object_name = 'produtos'
    template_name = 'saude_farmacia/produto.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade).order_by('nome_produto')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "produto":
            queryset = queryset.filter(nome_produto__icontains=self.request.GET.get('buscar_nome'))
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "codigo_de_barra":
            queryset = queryset.filter(codigo_de_barra=self.request.GET.get('buscar_nome'))
      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "produto"

        return context

class ProdutoCreateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, CreateView):
    model = Produto
    template_name = 'saude_farmacia/produto_create_update_form.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('saude_farmacia:produto_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class ProdutoUpdateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, UpdateView):
    model = Produto
    template_name = 'saude_farmacia/produto_create_update_form.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('saude_farmacia:produto_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class ProdutoDeleteView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, DeleteView):
    model = Produto
    template_name = "saude_farmacia/produto.html"
    success_url = reverse_lazy('saude_farmacia:produto_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class MedicamentoListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = Medicamento
    context_object_name = 'medicamentos'
    template_name = 'saude_farmacia/medicamento.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade).order_by('nome_medicamento')
        # queryset = super().get_queryset().all().order_by('nome_medicamento')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "medicamento":
            queryset = queryset.filter(nome_medicamento__icontains=self.request.GET.get('buscar_nome'))
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "codigo_de_barra":
            queryset = queryset.filter(codigo_de_barra=self.request.GET.get('buscar_nome'))
      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "medicamento"

        return context
    
class MedicamentoCreateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, CreateView):
    model = Medicamento
    template_name = 'saude_farmacia/medicamento_create_update_form.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('saude_farmacia:medicamento_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class MedicamentoUpdateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, UpdateView):
    model = Medicamento
    template_name = 'saude_farmacia/medicamento_create_update_form.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('saude_farmacia:medicamento_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.get_unidade_login().unidade
        return super().form_valid(form)

class MedicamentoDeleteView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, DeleteView):
    model = Medicamento
    template_name = "saude_farmacia/medicamento.html"
    success_url = reverse_lazy('saude_farmacia:medicamento_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class InsumoListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = Insumo
    context_object_name = 'insumos'
    template_name = 'saude_farmacia/insumo.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade).order_by('nome_insumo')
        # queryset = super().get_queryset().all().order_by('nome_insumo')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "insumo":
            queryset = queryset.filter(nome_insumo__icontains=self.request.GET.get('buscar_nome'))
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "codigo_de_barra":
            queryset = queryset.filter(codigo_de_barra=self.request.GET.get('buscar_nome'))
      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "insumo"

        return context

class InsumoCreateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, CreateView):
    model = Insumo
    template_name = 'saude_farmacia/insumo_create_update_form.html'
    form_class = InsumoForm
    success_url = reverse_lazy('saude_farmacia:insumo_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.get_unidade_login().unidade
        return super().form_valid(form)

class InsumoUpdateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, UpdateView):
    model = Insumo
    template_name = 'saude_farmacia/insumo_create_update_form.html'
    form_class = InsumoForm
    success_url = reverse_lazy('saude_farmacia:insumo_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.get_unidade_login().unidade
        return super().form_valid(form)

class InsumoDeleteView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, DeleteView):
    model = Insumo
    template_name = "saude_farmacia/insumo.html"
    success_url = reverse_lazy('saude_farmacia:insumo_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class RequisicaoMaterialFarmaciaListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = RequisicaoMaterialFarmacia
    # context_object_name = 'requisicoes'
    template_name = 'saude_farmacia/requisicao_material_farmacia.html'
    paginate_by=10
    
    def get_queryset(self):
        # queryset = super().get_queryset().filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade).order_by('codigo_setor')
        queryset = super().get_queryset().order_by('-data_solicitacao')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome_setor__icontains=self.request.GET.get("nome_filtro"))
        
        if self.request.GET.get("codigo_filtro"):
            queryset = queryset.filter(codigo_setor=self.request.GET.get("codigo_filtro"))
        
        if self.request.GET.get("sigla_filtro"):
            queryset = queryset.filter(sigla_setor=self.request.GET.get("sigla_filtro"))
        
        """
        if self.request.GET.get("setor_superior_filtro"):
            queryset = queryset.filter(setor_superior=self.request.GET.get("setor_superior_filtro"))
        
        if self.request.GET.get("situacao_filtro"):
            queryset = queryset.filter(situacao_setor=self.request.GET.get("situacao_filtro"))
        """

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['data_solicitacao_inicial_filtro'] = self.request.GET.get('data_solicitacao_inicial_filtro', '')
        context['data_solicitacao_final_filtro'] = self.request.GET.get('data_solicitacao_final_filtro', '')
        context['numero_pedido_filtro'] = self.request.GET.get('numero_pedido_filtro', '')

        context['listagem_select_farmaceutico_solicitante_busca'] = ['TODOS']
        for farmaceutico_solicitante in Profissional.objects.filter(situacao='ATIVO'):
            context['listagem_select_farmaceutico_solicitante_busca'].append(farmaceutico_solicitante)
        
        context['listagem_select_farmacia_busca'] = ['TODAS']
        for farmacia in Farmacia.objects.filter(situacao_farmacia=Farmacia.ATIVO):
            context['listagem_select_farmacia_busca'].append(farmacia)        

        context['situacoes'] = ['TODOS','ATIVO', 'INATIVO'] #Ajustar para ficar dinâmico

        context["requisicoes"] = self.get_queryset()
        return context

class RequisicaoMaterialFarmaciaCreateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, CreateView):
    model = RequisicaoMaterialFarmacia
    fields = ('numero_pedido', 'farmaceutico_solicitante', 'farmacia')
    template_name = 'saude_farmacia/requisicao_material_farmacia_create_update_form.html'
    paginate_by=10
    success_url = reverse_lazy('saude_farmacia:requisicao_material_farmacia_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = RequisicaoMaterialFarmaciaForm()
        context['form'].fields['farmacia'].queryset = Farmacia.objects.filter(situacao_farmacia=Farmacia.ATIVO, unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade)
        
        context['insumo_form'] = InsumoRequisitadoForm()
        context['medicamento_form'] = MedicamentoRequisitadoForm()
        context['produto_form'] = ProdutoRequisitadoForm()

        context['farmaceutico_solicitante'] = Profissional.objects.get(user=self.request.user)

        numero_registros = str(len(RequisicaoMaterialFarmacia.objects.all())).zfill(8)
        data  = datetime.date.today()
        ano = str(data.year)
        numero = ano + numero_registros
        context['numero'] = numero
        context['data_atual'] = datetime.datetime.today()

        return context

    def post(self, request, *args, **kwargs):
        form = RequisicaoMaterialFarmaciaForm(request.POST)
        insumo_form = InsumoRequisitadoForm(request.POST)
        medicamento_form = MedicamentoRequisitadoForm(request.POST)
        produto_form = ProdutoRequisitadoForm(request.POST)

        lista_material = request.POST.getlist('material')
        lista_tipo_material = request.POST.getlist('tipo_material')
        lista_quantidade_material = request.POST.getlist('quantidade_material')
        lista_unidade_material = request.POST.getlist('unidade_material')

        if form.is_valid():
            requisicao_material = form.save(commit=False)
            requisicao_material.farmaceutico_solicitante = Profissional.objects.get(user=self.request.user)
            requisicao_material.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
            requisicao_material.save()

            for pos in range(len(lista_material)):
                if lista_tipo_material[pos] == 'Produto':
                    produto = Produto.objects.get(id=lista_material[pos])
                    produto_requisitado = ProdutoRequisitado.objects.create(
                        produto=produto,
                        quantidade_produto=lista_quantidade_material[pos],
                        unidade_produto=lista_unidade_material[pos]
                    )
                    requisicao_material.produto_requisitado.add(produto_requisitado)

                elif lista_tipo_material[pos] == 'Insumo':
                    insumo = Insumo.objects.get(id=lista_material[pos])
                    insumo_requisitado = InsumoRequisitado.objects.create(
                        insumo=insumo,
                        quantidade_insumo=lista_quantidade_material[pos],
                        unidade_insumo=lista_unidade_material[pos]
                    )
                    requisicao_material.insumo_requisitado.add(insumo_requisitado)

                elif lista_tipo_material[pos] == 'Medicamento':
                    medicamento = Medicamento.objects.get(id=lista_material[pos])
                    medicamento_requisitado = MedicamentoRequisitado.objects.create(
                        medicamento=medicamento,
                        quantidade_medicamento=lista_quantidade_material[pos],
                        unidade_medicamento=lista_unidade_material[pos]
                    )
                    requisicao_material.medicamento_requisitado.add(medicamento_requisitado)

            return HttpResponseRedirect(self.success_url)

        context = {
            'form': form,
            'insumo_form': insumo_form,
            'medicamento_form': medicamento_form,
            'produto_form': produto_form,
        }

        return render(request, 'saude_farmacia/requisicao_material_farmacia_create_update_form.html', context)

class RequisicaoMaterialFarmaciaUpdateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, UpdateView):
    model = RequisicaoMaterialFarmacia
    template_name = 'saude_farmacia/requisicao_material_farmacia_create_update_form.html'
    form_class = RequisicaoMaterialFarmaciaForm
    context_object_name = "requisicao_material_farmacia"
    success_url = reverse_lazy('saude_farmacia:requisicao_material_farmacia_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        quantidade_materiais_por_pagina = 10

        context = super().get_context_data(**kwargs)

        context['farmaceutico_solicitante'] = self.get_object().farmaceutico_solicitante

        context['insumo_form'] = InsumoRequisitadoForm()
        context['medicamento_form'] = MedicamentoRequisitadoForm()
        context['produto_form'] = ProdutoRequisitadoForm()

        materiais = []


        for produto in self.get_object().produto_requisitado.all():
            materiais.append({
                "id": produto.produto.id,
                "valor": produto.produto.nome_produto,
                "codigo_de_barra": produto.produto.codigo_de_barra,
                "quantidade": produto.quantidade_produto,
                "unidade": produto.unidade_produto,
                "tipo": "Produto",
            })

        for insumo in self.get_object().insumo_requisitado.all():
            materiais.append({
                "id": insumo.insumo.id,
                "valor": insumo.insumo.nome_insumo,
                "codigo_de_barra": insumo.insumo.codigo_de_barra,
                "quantidade": insumo.quantidade_insumo,
                "unidade": insumo.unidade_insumo,
                "tipo": "Insumo",
            })

        for medicamento in self.get_object().medicamento_requisitado.all():
            materiais.append({
                "id": medicamento.medicamento.id,
                "valor": medicamento.medicamento.nome_medicamento,
                "codigo_de_barra": insumo.insumo.codigo_de_barra,
                "quantidade": medicamento.quantidade_medicamento,
                "unidade": medicamento.unidade_medicamento,
                "tipo": "Medicamento",
            })

        context["materiais"] = materiais
        context["quantidade_materiais_por_pagina"] = quantidade_materiais_por_pagina
        context["quantidade_paginas"] = range(1)

        return context

class RequisicaoMaterialFarmaciaDeleteView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, DeleteView):
    model = RequisicaoMaterialFarmacia
    template_name = "saude_farmacia/requisicao_material_farmacia.html"
    success_url = reverse_lazy('saude_farmacia:requisicao_material_farmacia_delete')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class EntradaMaterialFarmaciaListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = EntradaMaterialFarmacia
    context_object_name = 'entradas'
    template_name = 'saude_farmacia/entrada_material_farmacia.html'
    paginate_by=10
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade).order_by('-data_entrada')

        if self.request.GET.get("numero_pedido_filtro"):
            queryset = queryset.filter(numero_pedido__exact=self.request.GET.get("numero_pedido_filtro"))
        
        if self.request.GET.get("numero_nota_fiscal_filtro"):
            queryset = queryset.filter(numero_nota_fiscal__exact=self.request.GET.get("numero_nota_fiscal_filtro"))
        
        if self.request.GET.get("data_entrada_filtro"):
            data_entrada_filtro = self.request.GET.get("data_entrada_filtro")

            data_entrada_filtro = data_entrada_filtro.split("/")
            data_entrada_filtro = data_entrada_filtro[2]+"-"+data_entrada_filtro[1]+"-"+data_entrada_filtro[0]

            queryset = queryset.filter(data_entrada=data_entrada_filtro)
        
        if self.request.GET.get("farmacia_filtro"):
            queryset = queryset.filter(farmacia__id__exact=self.request.GET.get("farmacia_filtro"))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['numero_pedido_filtro'] = self.request.GET.get('numero_pedido_filtro', '')
        context['numero_nota_fiscal_filtro'] = self.request.GET.get('numero_nota_fiscal_filtro', '')

        context['data_entrada_filtro'] = self.request.GET.get('data_entrada_filtro', '')

        context['farmacia_filtro'] = ""

        if self.request.GET.get('farmacia_filtro', ''):
            context['farmacia_filtro'] = UUID(self.request.GET.get('farmacia_filtro', ''))
        
        context['farmacias'] = Farmacia.objects.filter(situacao_farmacia=Farmacia.ATIVO, unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade)
        
        return context

class EntradaMaterialFarmaciaCreateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, CreateView):
    model = EntradaMaterialFarmacia
    fields = ('numero_pedido', 'farmaceutico_responsavel', 'farmacia')
    template_name = 'saude_farmacia/entrada_material_farmacia_create_update_form.html'
    paginate_by=10
    success_url = reverse_lazy('saude_farmacia:entrada_material_farmacia_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = EntradaMaterialFarmaciaForm()

        context['form'].fields['farmacia'].queryset = Farmacia.objects.filter(situacao_farmacia=Farmacia.ATIVO, unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade)
        
        context['insumo_form'] = InsumoEntradaForm()
        context['medicamento_form'] = MedicamentoEntradaForm()
        context['produto_form'] = ProdutoEntradaForm()

        # context['farmaceutico_solicitante'] = Profissional.objects.get(user=self.request.user)

        
        # context['data_atual'] = datetime.datetime.today()

        return context

    def post(self, request, *args, **kwargs):
        form = EntradaMaterialFarmaciaForm(request.POST)
        insumo_form = InsumoEntradaForm(request.POST)
        medicamento_form = MedicamentoEntradaForm(request.POST)
        produto_form = ProdutoEntradaForm(request.POST)

        lista_material = request.POST.getlist('material')
        lista_tipo_material = request.POST.getlist('tipo_material')
        lista_quantidade_material = request.POST.getlist('quantidade_material')
        lista_unidade_material = request.POST.getlist('unidade_material')
        lista_numero_lote_material = request.POST.getlist('numero_lote_material')
        lista_data_vencimento_material = request.POST.getlist('data_vencimento_material')

        if form.is_valid():
            entrada_material = form.save(commit=False)
            entrada_material.farmaceutico_responsavel = Profissional.objects.get(user=self.request.user)
            entrada_material.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
            entrada_material.save()

            for pos in range(len(lista_material)):
                if lista_tipo_material[pos] == 'Produto':
                    data_vencimento_produto = lista_data_vencimento_material[pos].split("/")

                    produto = Produto.objects.get(id=lista_material[pos])
                    produto_entrada = ProdutoEntrada.objects.create(
                        unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade,
                        produto=produto,
                        quantidade_produto=lista_quantidade_material[pos],
                        unidade_produto=lista_unidade_material[pos],
                        numero_lote_produto=lista_numero_lote_material[pos],
                        data_vencimento_produto=f'{data_vencimento_produto[2]}-{data_vencimento_produto[1]}-{data_vencimento_produto[0]}'
                    )
                    entrada_material.produto_entrada.add(produto_entrada)

                elif lista_tipo_material[pos] == 'Insumo':
                    data_vencimento_insumo = lista_data_vencimento_material[pos].split("/")

                    insumo = Insumo.objects.get(id=lista_material[pos])
                    insumo_entrada = InsumoEntrada.objects.create(
                        unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade,
                        insumo=insumo,
                        quantidade_insumo=lista_quantidade_material[pos],
                        unidade_insumo=lista_unidade_material[pos],
                        numero_lote_insumo=lista_numero_lote_material[pos],
                        data_vencimento_insumo=f'{data_vencimento_insumo[2]}-{data_vencimento_insumo[1]}-{data_vencimento_insumo[0]}'
                    )
                    entrada_material.insumo_entrada.add(insumo_entrada)

                elif lista_tipo_material[pos] == 'Medicamento':
                    data_vencimento_medicamento = lista_data_vencimento_material[pos].split("/")

                    medicamento = Medicamento.objects.get(id=lista_material[pos])
                    medicamento_entrada = MedicamentoEntrada.objects.create(
                        unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade,
                        medicamento=medicamento,
                        quantidade_medicamento=lista_quantidade_material[pos],
                        unidade_medicamento=lista_unidade_material[pos],
                        numero_lote_medicamento=lista_numero_lote_material[pos],
                        data_vencimento_medicamento=f'{data_vencimento_medicamento[2]}-{data_vencimento_medicamento[1]}-{data_vencimento_medicamento[0]}'
                    )
                    entrada_material.medicamento_entrada.add(medicamento_entrada)
                
                entrada_material.save()

            return HttpResponseRedirect(self.success_url)

        context = {
            'form': form,
            'insumo_form': insumo_form,
            'medicamento_form': medicamento_form,
            'produto_form': produto_form,
        }

        return render(request, 'saude_farmacia/entrada_material_farmacia_create_update_form.html', context)

class EntradaMaterialFarmaciaUpdateView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, UpdateView):
    model = EntradaMaterialFarmacia
    template_name = 'saude_farmacia/entrada_material_farmacia_create_update_form.html'
    form_class = EntradaMaterialFarmaciaForm
    context_object_name = "entrada_material_farmacia"
    success_url = reverse_lazy('saude_farmacia:entrada_material_farmacia_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        quantidade_materiais_por_pagina = 10

        context = super().get_context_data(**kwargs)

        # context['farmaceutico_solicitante'] = self.get_object().farmaceutico_solicitante

        context['insumo_form'] = InsumoEntradaForm()
        context['medicamento_form'] = MedicamentoEntradaForm()
        context['produto_form'] = ProdutoEntradaForm()

        materiais = []


        for produto in self.get_object().produto_entrada.all():
            materiais.append({
                "id": produto.produto.id,
                "valor": produto.produto.nome_produto,
                "numero_lote": produto.numero_lote_produto,
                "quantidade": produto.quantidade_produto,
                "unidade": produto.unidade_produto,
                "data_vencimento": produto.data_vencimento_produto,
                "tipo": "Produto",
            })

        for insumo in self.get_object().insumo_entrada.all():
            materiais.append({
                "id": insumo.insumo.id,
                "valor": insumo.insumo.nome_insumo,
                "numero_lote": insumo.numero_lote_insumo,
                "quantidade": insumo.quantidade_insumo,
                "unidade": insumo.unidade_insumo,
                "data_vencimento": insumo.data_vencimento_insumo,
                "tipo": "Insumo",
            })

        for medicamento in self.get_object().medicamento_entrada.all():
            materiais.append({
                "id": medicamento.medicamento.id,
                "valor": medicamento.medicamento.nome_medicamento,
                "numero_lote": medicamento.numero_lote_medicamento,
                "quantidade": medicamento.quantidade_medicamento,
                "unidade": medicamento.unidade_medicamento,
                "data_vencimento": medicamento.data_vencimento_medicamento,
                "tipo": "Medicamento",
            })

        context["materiais"] = materiais
        context["quantidade_materiais_por_pagina"] = quantidade_materiais_por_pagina
        context["quantidade_paginas"] = range(1)

        return context
    
    def form_valid(self, form):
        instancia = form.save(commit=False)

        instancia.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade

        lista_material = self.request.POST.getlist('material')
        lista_tipo_material = self.request.POST.getlist('tipo_material')
        lista_quantidade_material = self.request.POST.getlist('quantidade_material')
        lista_unidade_material = self.request.POST.getlist('unidade_material')
        lista_numero_lote_material = self.request.POST.getlist('numero_lote_material')
        lista_data_vencimento_material = self.request.POST.getlist('data_vencimento_material')

        # form.save()

        # requisicao_material_farmacia = RequisicaoMaterialFarmacia.objects.get(pk=self.kwargs["pk"])

        # requisicao_material_farmacia.farmaceutico_solicitante = Profissional.objects.get(user=self.request.user)

        insumos_entradas = []
        medicamentos_entradas = []


        for pos in range(len(lista_material)):
            if lista_tipo_material[pos] == 'Insumo':
                # data_vencimento_insumo = lista_data_vencimento_material[pos].split("-")

                insumo = Insumo.objects.get(id=lista_material[pos])
                insumo_entrada = InsumoEntrada.objects.get_or_create(
                    unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade,
                    insumo=insumo,
                    quantidade_insumo=lista_quantidade_material[pos],
                    unidade_insumo=lista_unidade_material[pos],
                    numero_lote_insumo=lista_numero_lote_material[pos],
                    data_vencimento_insumo=lista_data_vencimento_material[pos]
                )
                insumos_entradas.append(UUID(insumo_entrada.id))

            elif lista_tipo_material[pos] == 'Medicamento':
                # data_vencimento_medicamento = lista_data_vencimento_material[pos].split("-")

                medicamento = Medicamento.objects.get(id=lista_material[pos])
                medicamento_entrada, create = MedicamentoEntrada.objects.get_or_create(
                    unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade,
                    medicamento=medicamento,
                    quantidade_medicamento=lista_quantidade_material[pos],
                    unidade_medicamento=lista_unidade_material[pos],
                    numero_lote_medicamento=lista_numero_lote_material[pos],
                    data_vencimento_medicamento=lista_data_vencimento_material[pos]
                )
                medicamentos_entradas.append(medicamento_entrada)

        instancia.insumo_entrada.set(insumos_entradas)

        medicamentos_entradas_id = [medicamento.id for medicamento in medicamentos_entradas]
        instancia.medicamento_entrada.set(medicamentos_entradas_id)

        instancia.save()


        # form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class EntradaMaterialFarmaciaDeleteView(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, DeleteView):
    model = EntradaMaterialFarmacia
    template_name = "saude_farmacia/entrada_material_farmacia.html"
    success_url = reverse_lazy('saude_farmacia:entrada_material_farmacia_delete')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class ControleEstoqueMedicamentoListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = MedicamentoEntrada
    context_object_name = 'medicamentos'
    template_name = 'saude_farmacia/controle_estoque_medicamento.html'
    paginate_by=10

    def get_queryset(self):
        data_atual = datetime.datetime.now()
        data_daqui_90_dias = data_atual + datetime.timedelta(days=90)

        entradas_materiais = EntradaMaterialFarmacia.objects.all().only('medicamento_entrada')

        medicamentos_id = []

        for entrada in entradas_materiais:
            medicamentos_filtrados_id = entrada.medicamento_entrada.filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade, data_vencimento_medicamento__range=(data_atual, data_daqui_90_dias), medicamento__quantidade__gt=0).values_list("pk", flat=True)
            
            medicamentos_id.extend(medicamentos_filtrados_id)
        

        # queryset = super().get_queryset().filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade, data_vencimento_medicamento__range=(data_atual, data_daqui_90_dias), medicamento__quantidade__gt=0).order_by("data_vencimento_medicamento", "medicamento__nome_medicamento")
        queryset = super().get_queryset().filter(pk__in=medicamentos_id).order_by("data_vencimento_medicamento", "medicamento__nome_medicamento")

        if self.request.GET.get("nome_medicamento_filtro"):
            queryset = queryset.filter(medicamento__nome_medicamento__icontains=self.request.GET.get("nome_medicamento_filtro"))

        if self.request.GET.get("numero_lote_filtro"):
            queryset = queryset.filter(numero_lote_medicamento__exact=self.request.GET.get("numero_lote_filtro"))
        
        if self.request.GET.get("data_vencimento_filtro"):
            data_vencimento_filtro = self.request.GET.get("data_vencimento_filtro")

            data_vencimento_filtro = data_vencimento_filtro.split("/")
            data_vencimento_filtro = data_vencimento_filtro[2]+"-"+data_vencimento_filtro[1]+"-"+data_vencimento_filtro[0]

            queryset = queryset.filter(data_vencimento_medicamento=data_vencimento_filtro)
        
        if self.request.GET.get("quantidade_em_estoque_filtro"):
            queryset = queryset.filter(medicamento__quantidade__exact=self.request.GET.get("quantidade_em_estoque_filtro"))
      
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_medicamento_filtro'] = self.request.GET.get('nome_medicamento_filtro', '')
        context['numero_lote_filtro'] = self.request.GET.get('numero_lote_filtro', '')

        context['data_vencimento_filtro'] = self.request.GET.get('data_vencimento_filtro', '')

        context['quantidade_em_estoque_filtro'] = self.request.GET.get('quantidade_em_estoque_filtro', '')

        return context
    
class MedicamentoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        query = Medicamento.objects.all()

        if self.q:
            query = query.filter(nome_medicamento__istartswith=self.q)

        return query