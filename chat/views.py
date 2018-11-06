# chat/views.py
import time
import uuid
import html
import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from chat.models import User, Group, GroupChat, ImageModel, FileModel, Message
from chat.consumers import channel_publish
from django.conf import settings
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def home(request):
	user_id = request.GET.get('user_id', None)
	if user_id is not None:
		user = User.objects.get(id=user_id)
		return render(request, 'chat/chat.html', {'id': user_id})
	return render(request, 'chat/chat.html', {'user_id': user_id})


@csrf_exempt
def msg_gateway(request):
	'''
	接收客户端发送的消息
	:param request:
	:return:
	'''
	if request.method == 'POST':
		# print(request.POST)
		from_user_name = request.POST.get('mine[username]', None)
		from_user_avatar = request.POST.get('mine[avatar]', None)
		from_user_id = request.POST.get('mine[id]', None)
		content = request.POST.get('mine[content]', None)
		
		# 消息接收方
		to_user = request.POST.get('to[name]', None)
		# 好友类型
		user_type = request.POST.get('to[type]', None)
		# 如果是群聊里的消息，这个是群聊的ID
		# 如果是私聊的消息，则是对方的ID
		to_user_id = request.POST.get('to[id]', None)
		# msg中的id字段表示的消息来源ID
		# 如果是群聊消息则是to_user_id
		# 如果是私聊消息则是from_user_id
		id_ = from_user_id
		mine = False
		timestamp = int(time.time() * 1000)
		if 'group' == user_type:
			id_ = to_user_id
			# mine = True
		msg = {
			# 消息来源用户名
			'username': from_user_name,
			# 消息来源用户头像
			'avatar': from_user_avatar,
			# 消息的来源ID（如果是私聊，则是用户id，如果是群聊，则是群组id）
			'id': id_,
			'type': user_type,
			'content': content,
			# 消息id，可不传。除非你要对消息进行一些操作（如撤回）
			'cid': 0,
			# 是否我发送的消息，如果为true，则会显示在右方
			'mine': mine,
			# 消息的发送者id（比如群组中的某个消息发送者），可用于自动解决浏览器多窗口时的一些问题
			'fromid': from_user_id,
			'timestamp': timestamp,
		}
		Message.objects.create(
			from_user_id=from_user_id,
			from_user_name=from_user_name,
			from_user_avatar=from_user_avatar,
			to_user_or_group_id=to_user_id,
			channel_type=user_type,
			content=content,
			timestamp=timestamp,
		)
		content = {
			'channel_type': 'msg',
			'msg': msg,
		}
		channel_publish(to_user_id, content)
		return JsonResponse({'code': 0, 'status': True, 'info': '消息发送成功'})
	

@csrf_exempt
def history_msg(request):
	'''
	获取聊天记录
	id=bc050bc4-a124-4aa7-a267-cc2a6803169e&type=group
	:param request:
	:return:
	'''
	res = dict()
	type = request.GET.get('type', None)
	# 好友ID或群聊ID
	id = request.GET.get('id', None)
	# 当前用户ID
	user_id = request.GET.get('user_id', None)
	if 'friend' == type:
		# 好友发送给当前用户的消息
		# 当前用户发送给好友的消息
		# msg1 = Message.objects.filter(from_user_id=user_id, to_user_or_group_id=id)
		data = [
			{
				'username': msg.from_user_name,
				'id': msg.id,
				'avatar': msg.from_user_avatar,
				'timestamp': msg.timestamp,
				'content': msg.content,
			}
			for msg in Message.objects.filter(from_user_id__in=[id, user_id], to_user_or_group_id__in=[id, user_id]).order_by('timestamp')
		]
		res['code'] = 0
		res['msg'] = ''
		res['data'] = data
		return JsonResponse(res)
	else:
		data = [
			{
				'username': msg.from_user_name,
				'id': msg.id,
				'avatar': msg.from_user_avatar,
				'timestamp': msg.timestamp,
				'content': msg.content,
			}
			for msg in Message.objects.filter(to_user_or_group_id=id)
		]
		res['code'] = 0
		res['data'] = data
		return JsonResponse(res)
	

def init_user(request):
	'''
	初始化用户聊天界面
	:param request:
	:return:
	'''
	res = {
		'code': -1,
		'msg': '初始化',
		'data': {
			'mine': {
			
			},
			'friend': [
			
			],
			'group': [
			
			]
		}
	}
	user_id = request.GET.get('user_id', None)
	# print('user_id', user_id)
	if user_id is None:
		res['msg'] = 'user_id is None'
		return JsonResponse(res)
	
	# 查询用户的好友分组
	groups = Group.objects.filter(owner=user_id)
	friends = list()
	for item in groups:
		# print('group', item.name)
		friend_list = [
			{
				'username': fri.username,
				'id': fri.id,
				'avatar': fri.avatar,
				'sign': fri.signature,
				'status': fri.get_status_display()
			}
			for fri in item.group_members.all()
		]
		group_friends = {
			'groupname': item.name,
			'id': item.id,
			'list': friend_list,
		}
		friends.append(group_friends)
	# print(friends)
	# 好友列表
	res['data']['friend'] = friends
	
	# 群组列表
	user = User.objects.get(pk=user_id)
	group_chats = user.group_chat_members.all()
	res['data']['group'] = [{'groupname': item.name, 'id': item.id, 'avatar': item.group_chat_avatar} for item in group_chats]
	
	# 我的信息
	res['data']['mine'] = {
		'username': user.username,
		'id': user.id,
		'status': 'online',
		'sign': user.signature,
		'avatar': user.avatar,
	}
	res['code'] = 0
	return JsonResponse(res)


def init_group_chat(request):
	'''
	获取用户群聊信息
	:param request:
	:return:
	'''
	# 获取layim框架传递的群聊ID
	group_chat_id = request.GET.get('id', None)
	res = {
		'code': 0,
		'msg': '',
		'data': {
			'list': [
			
			]
		}
	}
	if group_chat_id is None:
		res['msg'] = 'group_chat_id is None'
		return JsonResponse(res)
	group_chat = GroupChat.objects.get(id=group_chat_id)
	res['data']['list'] = [
					{
						'username': item.username,
						'id': item.id,
						'avatar': item.avatar,
						'sign': item.signature
					}
					for item in group_chat.group_chat_members.all()
	]
	
	return JsonResponse(res)


@csrf_exempt
def add_friend(request):
	'''
	添加好友
	:param request:
	:return:
	'''
	res_type = request.POST.get('res_type', None)
	# 用户A申请添加用户B为好友
	if 'add' == res_type:
		# 申请添加好友的用户ID
		a_user_id = request.POST.get('user_id', None)
		# 被添加的用户ID
		b_friend_id = request.POST.get('friend_id', None)
		# 目标好友组
		to_group_id = request.POST.get('to_group_id', None)
		# 好友申请信息
		remark = request.POST.get('remark', None)
		# print('用户A的ID', a_user_id)
		user = User.objects.get(pk=a_user_id)
		friend = User.objects.get(pk=b_friend_id)
		# print('%s要添加%s为好友' % (user.username, friend.username))
		# 向用户B发送好友申请
		content = {
			'channel_type': 'be_added_as_a_friend',
			'msg': {
				'type': 'friend',
				'username': user.username,
				'avatar': user.avatar,
				'from_user_id': a_user_id,
				'id': a_user_id,
				'to_group_id': to_group_id,
				# 'groupid': to_group_id,
				# 'sign': user.signature,
			},
		}
		channel_publish(b_friend_id, content)
		return JsonResponse({'code': 0, 'status': True, 'info': '好友申请已发送'})
	# 用户B同意用户A的好友申请
	elif 'pass' == res_type:
		# 申请添加好友的用户ID
		user_id = request.POST.get('user_id', None)
		user = User.objects.get(id=user_id)
		# 被添加的用户ID
		friend_id = request.POST.get('friend_id', None)
		# 用户A的好友组
		a_group_id = request.POST.get('a_group_id', None)
		# 用户B的好友组
		b_group_id = request.POST.get('b_group_id', None)
		
		friend = User.objects.get(id=friend_id)
		# 获取好友组
		a_group = Group.objects.get(id=a_group_id)
		a_group.group_members.add(friend)
		b_group = Group.objects.get(pk=b_group_id)
		b_group.group_members.add(user)
		# print('%s同意了%s的好友申请' % (friend.username, user.username))
		# 向用户A通知申请通过
		a_content = {
			'channel_type': 'friend_result',
			'type': 'pass',
			'msg': {
				'type': 'friend',
				'avatar': friend.avatar,
				'username': friend.username,
				'groupid': a_group_id,
				'id': friend_id,
				'sign': friend.signature,
			},
		}
		
		b_content = {
			'type': 'pass',
			'msg': {
				'type': 'friend',
				'avatar': user.avatar,
				'username': user.username,
				'groupid': b_group_id,
				'id': user_id,
				'sign': user.signature,
			},
		}
		channel_publish(user_id, a_content)
		return JsonResponse(b_content['msg'])
	

@csrf_exempt
def apply_group_chat(request):
	'''
	申请加入群聊
	:param request:
	:return:
	'''
	if request.method == 'POST':
		res_type = request.POST.get('res_type', None)
		user_id = request.POST.get('user_id', None)
		group_chat_id = request.POST.get('group_chat_id', None)
		remark = request.POST.get('remark', None)
		user = User.objects.get(pk=user_id)
		# 给群聊管理员发送申请通知
		group_chat = GroupChat.objects.get(pk=group_chat_id)
		admins = group_chat.group_admins.all()
		content = {
			'channel_type': 'apply_group_chat',
			'msg': {
				'type': 'group',
				'username': user.username,
				'avatar': user.avatar,
				'groupid': group_chat_id,
				'id': user_id,
				'sign': user.signature
			},
		}
		# print('发送消息')
		for admin in admins:
			channel_publish(str(admin.id), content)
		return JsonResponse({'code': 0, 'status': True, 'info': '申请已发送'})
		

@csrf_exempt
def search_friend(request):
	'''
	搜索好友
	:param request:
	:return:
	'''
	res = {
		'code': 0,
		'msg': '',
		'count': 0,
		'data': []
	}
	if request.method == 'POST':
		key_word = request.POST.get('key_word', None)
		search_type = request.POST.get('search_type', None)
		user_id = request.POST.get('user_id', None)
		if not key_word or not search_type:
			res['code'] = -1
			res['msg'] = 'invalid parameters'
			return JsonResponse(res)
		# 搜好友
		if int(search_type) == 0:
			result = [
				{
					'username': user.username,
					'id': user.id,
					'sex': user.get_sex_display(),
					'sign': user.signature,
					'avatar': user.avatar
				}
				for user in User.objects.filter(username__icontains=key_word) if str(user.id) != user_id
			]
			res['count'] = len(result)
			res['data'] = result
		else:
			result = [
				{
					'id': group_chat.id,
					'group_chat_name': group_chat.name,
					'avatar': group_chat.group_chat_avatar
				}
				for group_chat in GroupChat.objects.filter(name__icontains=key_word)
			]
			res['count'] = len(result)
			res['data'] = result
		return JsonResponse(res)


@csrf_exempt
def upload_image(request):
	'''
	上传图片
	:param request:
	:return:
	'''
	res = {
		'code': -1,
		'msg': '',
		'data': {
		}
	}
	if request.method == 'POST':
		pic = request.FILES.get('file')
		pic.name = str(uuid.uuid4()) + '.' + pic.name.rsplit('.', 1)[1]
		image = ImageModel.objects.create(model_pic=pic)
		# qiniu_upload(pic)
		# print(image.model_pic.name)
		res['code'] = 0
		date = datetime.datetime.now().strftime("%y%m%d")
		res['data']['src'] = '%s/statics/upload/%s/%s' % (settings.Domain, date, pic.name)
		# print(res)
		return JsonResponse(res)
	res['msg'] = '上传文件失败'
	return JsonResponse(res)


@csrf_exempt
def upload_avatar(request):
	'''
	用户上传头像
	:param request:
	:return:
	'''
	res = {
		'code': -1,
		'msg': '',
		'data': {
		}
	}
	if request.method == 'POST':
		user_id = request.GET.get('user_id', None)
		pic = request.FILES.get('file')
		pic.name = str(uuid.uuid4()) + '.' + pic.name.rsplit('.', 1)[1]
		image = ImageModel.objects.create(model_pic=pic)
		res['code'] = 0
		date = datetime.datetime.now().strftime("%y%m%d")
		res['data']['src'] = '%s/statics/upload/%s/%s' % (settings.Domain, date, pic.name)
		user = User.objects.get(pk=user_id)
		user.avatar = res['data']['src']
		user.save()
		# print(res)
		return JsonResponse(res)
	res['msg'] = '上传文件失败'
	return JsonResponse(res)


@csrf_exempt
def upload_file(request):
	'''
	上传文件
	:param request:
	:return:
	'''
	res = {
		'code': -1,
		'msg': '',
		'data': {
		}
	}
	if request.method == 'POST':
		file_ = request.FILES.get('file')
		file_.name = str(uuid.uuid4()) + '.' + file_.name.rsplit('.', 1)[1]
		file_model = FileModel.objects.create(model_file=file_)
		# qiniu_upload(pic)
		# print(file_model.model_file.name)
		res['code'] = 0
		date = datetime.datetime.now().strftime("%y%m%d")
		res['data']['src'] = '%s/statics/upload/%s/%s' % (settings.Domain, date, file_.name)
		# print(res)
		return JsonResponse(res)
	res['msg'] = '上传文件失败'
	return JsonResponse(res)


@csrf_exempt
def modify_sign(request):
	'''
	用户修改签名
	:param request:
	:return:
	'''
	if request.method == 'POST':
		sign = request.POST.get('sign', None)
		user_id = request.POST.get('id', None)
		# print('sign', sign)
		# print('user_id', user_id)
		if sign and user_id:
			user = User.objects.get(pk=user_id)
			user.signature = sign
			user.save()
			return JsonResponse({'code': 0, 'msg': 'success'})
		return JsonResponse({'code': -1, 'msg': 'invalid parameters'})
	

@csrf_exempt
def modify_status(request):
	'''
	用户修改状态
	:param request:
	:return:
	'''
	if request.method == 'POST':
		status = request.POST.get('status', None)
		user_id = request.POST.get('id', None)
		# print('sign', status)
		# print('user_id', user_id)
		if status and user_id:
			user = User.objects.get(pk=user_id)
			user.status = 'ON' if status == 'online' else 'OFF'
			user.save()
			return JsonResponse({'code': 0, 'msg': 'success'})
		return JsonResponse({'code': -1, 'msg': 'invalid parameters'})
	

@csrf_exempt
def group_chat_ids(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id', None)
		if not user_id:
			return JsonResponse({'code': -1, 'msg': 'invalid parameters'})
		user = User.objects.get(pk=user_id)
		group_chats = user.groupchat_set.all()
		data = [item.id for item in group_chats]
		return JsonResponse({'code': 0, 'msg': '', 'data': data})
	

@csrf_exempt
def add_group_chat(request):
	'''
	新建群聊
	创建者默认是群聊的管理员
	:param request:
	:return:
	'''
	if request.method == 'POST':
		user_id = request.POST.get('user_id', None)
		group_chat_name = request.POST.get('group_chat_name', None)
		group_chat_avatar = request.POST.get('group_chat_avatar', None)
		if not group_chat_name or not user_id:
			return JsonResponse({'code': -1, 'msg': 'invalid parameters'})
		user = User.objects.get(pk=user_id)
		group_chat = GroupChat.objects.create(name=group_chat_name)
		group_chat.group_admins.add(user)
		group_chat.group_chat_members.add(user)
		return JsonResponse({'code': 0, 'msg': '', 'data': {'group_id': group_chat.id, 'group_avatar': group_chat.group_chat_avatar}})


@csrf_exempt
def add_group(request):
	'''
	新建好友分组
	:param request:
	:return:
	'''
	if request.method == 'POST':
		user_id = request.POST.get('user_id', None)
		group_name = request.POST.get('group_name', None)
		group_avatar = request.POST.get('group_avatar', None)
		if not group_name or not user_id:
			return JsonResponse({'code': -1, 'msg': 'invalid parameters'})
		user = User.objects.get(pk=user_id)
		group = Group.objects.create(name=group_name, owner=user)
		return JsonResponse({'code': 0, 'msg': '', 'data': {'group_id': group.id}})
	

@csrf_exempt
def user_info(request):
	if request.method == 'GET':
		user_id = request.GET.get('user_id', None)
		if user_id:
			user = User.objects.get(pk=user_id)
			return render(request, 'chat/user_info.html', context={'user': user})
		return render(request, 'chat/user_info.html')
	else:
		signature = request.POST.get('signature', None)
		email = request.POST.get('email', None)
		# city = request.POST.get('city', None)
		birthday = request.POST.get('birthday', None)
		phone = request.POST.get('phone', None)
		user_id = request.POST.get('user_id', None)
		if not user_id:
			return JsonResponse({'code': -1, 'status': False, 'info': 'invalid user_id'})
		user = User.objects.get(pk=user_id)
		user.signature = signature
		user.email = email
		user.birthday = birthday
		user.phone = phone
		user.save()
		return JsonResponse({'code': 0, 'status': True, 'info': '修改成功'})