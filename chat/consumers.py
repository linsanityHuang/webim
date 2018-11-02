# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


class ChatConsumer(AsyncWebsocketConsumer):
	
	# 当 websocket 一链接上以后触发该函数
	# self.scope可以类比的理解为django中的self.request
	# 从url中取出room_name字段备用，这里的变量名是在路由中设置的
	async def connect(self):
		# print(self.scope['url_route'])
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = self.room_name
		
		# Join room group
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()
	
	# 断开链接是触发该函数
	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	# 前端发送来消息时，通过这个接口传递
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		# Send message to room group
		# 这里的type要在当前类中实现一个相应的函数，
		# 下划线或者'.'的都会被Channels转换为下划线处理，
		# 所以这里写 'chat.message'也没问题
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat.message',
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


def channel_publish(topic, content):
	try:
		'''
		type需要与consumer中的receive中一致
		group_name是consumer中的room_group_name
		'''
		async_to_sync(channel_layer.group_send)(
			topic,
			{
				'type': 'chat.message',
				'message': content,
			}
		)
	except Exception as e:
		raise e