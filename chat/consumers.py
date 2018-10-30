# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.channel_group_name = self.scope['url_route']['kwargs']['channel_group_name']

		# Join room group
		await self.channel_layer.group_add(
			self.channel_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(
			self.channel_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		# Send message to room group
		await self.channel_layer.group_send(
			self.channel_group_name,
			{
				'type': 'chat_message',
				'message': message
			}
		)

	# Receive message from room group
	async def chat_message(self, event):
		message = event['message']

		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'message': message
		}))


# channels发送通知到页面
channel_layer = get_channel_layer()


def publish(topic, content):
	try:
		'''
		type需要与consumer中的receive中一致
		group_name是consumer中的room_group_name
		'''
		async_to_sync(channel_layer.group_send)(
			topic,
			content
		)
	except Exception as e:
		raise e