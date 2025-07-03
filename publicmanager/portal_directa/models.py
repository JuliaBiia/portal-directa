from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SolicitacaoAlvaraFuncionamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    # Dados do solicitante
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Solicitante')
    nome_estabelecimento = models.CharField(max_length=200, verbose_name='Nome do Estabelecimento')
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ')
    endereco = models.CharField(max_length=300, verbose_name='Endereço')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    email = models.EmailField(verbose_name='E-mail')
    
    # Dados da atividade
    atividade_principal = models.TextField(verbose_name='Atividade Principal')
    area_construida = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Área Construída (m²)')
    numero_funcionarios = models.IntegerField(verbose_name='Número de Funcionários')
    
    # Controle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    data_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name='Data da Solicitação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    class Meta:
        verbose_name = 'Solicitação de Alvará de Funcionamento'
        verbose_name_plural = 'Solicitações de Alvará de Funcionamento'
        ordering = ['-data_solicitacao']
    
    def __str__(self):
        return f"{self.nome_estabelecimento} - {self.get_status_display()}"
