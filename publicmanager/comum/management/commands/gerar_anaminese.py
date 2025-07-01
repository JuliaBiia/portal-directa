from django.core.management.base import BaseCommand

from publicmanager.saude_atendimento.models import Paciente, AnamnesePaciente

class Command(BaseCommand):
    help = 'Gerar Anaminese'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Gerarando Anaminese ...'))

        pacientes = Paciente.objects.all()

        for paciente in pacientes:
            anamnese_paciente = AnamnesePaciente.objects.create()

            paciente.anamnese_paciente = anamnese_paciente
            paciente.save()


        self.stdout.write(self.style.SUCCESS('Anaminese criadas sucesso!'))