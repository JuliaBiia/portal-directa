from django.db import models
from django.conf import settings
from django_lifecycle import hook
from django.utils.timezone import now
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from publicmanager.comum.models import BaseModel
from publicmanager.saude.models import UnidadeSaude

# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self, cpf_cnpj, email, nome, password=None):
        if not cpf_cnpj:
            raise ValueError('Um CPF deve ser especificado')
        if not email:
            raise ValueError('Um e-mail deve ser especificado')
        if not nome:
            raise ValueError('Um nome deve ser especificado')
        email_normalizado = self.normalize_email(email)
        usuario = self.model(cpf_cnpj=cpf_cnpj, email=email_normalizado, nome=nome)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, cpf_cnpj, email, nome, password):
        usuario = self.create_user(cpf_cnpj, email, nome, password)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)

class Usuario(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'cpf_cnpj'
    REQUIRED_FIELDS = ['nome', 'email']

    cpf_cnpj = models.CharField(max_length=14, unique=True, error_messages={'unique': 'Um usuário com esse cpf/cnpj já foi cadastrado.'}, verbose_name='CPF/CNPJ')
    email = models.EmailField(unique=True, error_messages={'unique': 'Um usuário com esse e-mail já foi cadastrado.'}, verbose_name='E-mail')
    nome = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_staff = models.BooleanField(default=False)
    suporte = models.BooleanField(default=False, verbose_name='É Suporte?')
    deve_mudar_senha = models.BooleanField('Deve mudar a senha no próximo acesso', default=False)

    objects = UsuarioManager()

    def __str__(self):
        return f'{self.nome} ({self.cpf_cnpj})'
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    @property
    def tipo_usuario(self):
        from publicmanager.saude_cadastro.models import Profissional
        painel_unidade_usuario = PainelUnidadeUsuario.objects.filter(usuario=self).first()
        
        if painel_unidade_usuario:
            return settings.PAINEL
        
        if  self.profissional_set.exists():
            profissional = self.profissional_set.first()

            if profissional.tipo_profissional == Profissional.MEDICO:
                return settings.MEDICO
            elif profissional.tipo_profissional == Profissional.ENFERMEIRO:
                return settings.ENFERMEIRO
            elif profissional.tipo_profissional == Profissional.RECEPCIONISTA:
                return settings.RECEPCIONISTA
            elif profissional.tipo_profissional == Profissional.RADIOLOGISTA:
                return settings.RADIOLOGISTA
            elif profissional.tipo_profissional == Profissional.SUPORTE:
                return settings.SUPORTE
            elif profissional.tipo_profissional == Profissional.DESENVOLVEDOR:
                return settings.DESENVOLVEDOR
            elif profissional.tipo_profissional == Profissional.FARMACEUTICO:
                return settings.FARMACEUTICO
            elif profissional.tipo_profissional == Profissional.ADMINISTRADO:
                return settings.ADMINISTRADO
            elif profissional.tipo_profissional == Profissional.TECNICO_ENFERMAGEM:
                return settings.TECNICO_ENFERMAGEM
            
            elif profissional.tipo_profissional == Profissional.NUTRICIONISTA:
                return settings.NUTRICIONISTA
            
            return None
        return None
    
    def get_unidade_login(self):
        painel_unidade_usuario = PainelUnidadeUsuario.objects.filter(usuario=self).first()

        if painel_unidade_usuario:
            return painel_unidade_usuario
        
        if  self.profissional_set.exists() and self.profissional_set.first().unidadelogin:
            return self.profissional_set.first().unidadelogin
        return None
    
    def update_password(self, reset=False):
        active_sessions = Session.objects.filter(expire_date__gt=now())
        for session in active_sessions:
            data = session.get_decoded()
            if data.get('_auth_user_id') == str(self.id):
                session.delete()
        
        self.set_password(self.cpf_cnpj)
        if reset:
            self.deve_mudar_senha = True
        self.save()

class PainelUnidadeUsuario(BaseModel):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT, related_name='painel_unidade_usuario', verbose_name="Usuário do Painel")
    unidade = models.ForeignKey(UnidadeSaude, on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Painel Unidade Usuário'
        verbose_name_plural = 'Paineis Unidade Usuário'

    def __str__(self):
        return f'{self.usuario} - {self.unidade}'
    
class RegistroAcesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    endereco_ip = models.GenericIPAddressField(verbose_name="Endereço IP")
    caminho = models.CharField(max_length=200, verbose_name="Caminho")
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")
    descricao = models.TextField("Descrição", blank=True, null=True)

    class Meta:
        verbose_name = "Registro de acesso"
        verbose_name_plural = "Registros de acesso"
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.usuario} - {self.endereco_ip} - {self.caminho} - {self.data_hora}"