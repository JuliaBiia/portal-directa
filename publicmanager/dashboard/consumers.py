import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer

class PainelChamadaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.slug1 = self.scope['url_route']['kwargs']['slug1']
        self.slug2 = self.scope['url_route']['kwargs']['slug2']
        self.group_name = f'painel_{self.slug1.replace("-", "_")}_{self.slug2.replace("-", "_")}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        print("Conexão WebSocket aceita.")

        self.ping_task = asyncio.create_task(self.send_ping())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        self.ping_task.cancel()

    async def update_panel(self, event):
        await self.send(text_data=json.dumps({
            'contagem': event['contagem'],
            'paciente': event['paciente'],
            'tipo_setor': event['tipo_setor'],
            'sala': event['sala'],
        }))

    async def send_ping(self):
        print('Enviando ping...')
        try:
            while True:
                await asyncio.sleep(60)
                await self.send(text_data=json.dumps({'ping': 'ping'}))
        except asyncio.CancelledError:
            print('Ping task cancelled')


class AtualizarListagensConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.slug1 = self.scope['url_route']['kwargs']['slug1']
        self.group_name = f'atualizar_listagem_{self.slug1.replace("-", "_")}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def update_listagem(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'paciente': event['paciente'],
            'tipo_setor': event['tipo_setor'],
        }))