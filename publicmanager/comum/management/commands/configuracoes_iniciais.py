from django.core import management
from django.core.management.base import BaseCommand

from publicmanager.autenticacao.models import Usuario

class Command(BaseCommand):
    help = 'Configurações Iniciais do Projeto'

    def handle(self, *args, **kwargs):
        nome = 'admin'
        email = 'admin@example.com'
        password = 'onegov@v12024'
        cpf = '12345'

        try:
            #Gerar os bancos.
            management.call_command('importar_bancos')
            print("Finalizou a importação dos bancos")

            #Gerar os paises.
            management.call_command('importar_paises')
            print("Finalizou a importação dos paises")
            
            #Gerar os municipios.
            management.call_command('importar_municipios')
            print("Finalizou a importação dos municipios")

            #Gerar profissões.
            management.call_command('importar_profissoes')
            print("Profissões geradas")

            # Verifica se o usuário admin já existe
            if Usuario.objects.filter(nome=nome).exists():
                self.stdout.write(self.style.SUCCESS(f'O usuário "{nome}" já existe. Nenhuma ação realizada.'))
            else:
                # Cria o usuário admin
                user = Usuario.objects.create_superuser(cpf, nome, email, password)
                self.stdout.write(self.style.SUCCESS(f'Usuário admin "{nome}" criado com sucesso.'))

        except Exception as e:
            print(e)