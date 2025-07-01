from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'Deslogar todos os usuários, removendo todas as sessões ativas.'

    def handle(self, *args, **kwargs):
        active_sessions_count = Session.objects.count()

        num_sessions_deleted, _ = Session.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f'Antes da remoção, havia {active_sessions_count} sessões ativas. '
            f'{num_sessions_deleted} sessões foram deletadas com sucesso. Todos os usuários foram deslogados.'
        ))
