import html
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt
from chat.models import User, Group


@csrf_exempt
def do_login(request):
	'''
	执行登录逻辑，登录成功跳往聊天界面
	:param request:
	:return:
	'''
	if request.method == 'POST':
		# print('do_login post')
		username = request.POST.get('username', None)
		username = html.escape(username)
		password = request.POST.get('password', None)
		password = html.escape(password)
		# print('username', username)
		# print('password', password)
		# user = authenticate(request, username=username, password=password)
		user = User.objects.filter(username=username, password=password)
		# print(user)
		if user.count() == 1:
			# 查询好友，群组，历史记录
			# login(request, user)
			# todo
			# print('已登录')
			# print(user[0].status)
			user[0].status = 'ON'
			# print(user[0].status)
			user[0].save()
			return JsonResponse({'code': 0, 'status': True, 'info': '登录成功', 'user_id': user[0].id})
			# return render(request, 'chat/chat_pc.html', context={'user_id': user[0].id})
			# return HttpResponseRedirect(reverse('chat_pc'))
		else:
			# print('用户不存在')
			return render(request, 'login/login.html', {'username': username, 'password': password})
	# print('do_login get')
	return render(request, 'login/login.html')


@csrf_exempt
def signin(request):
	'''
	用户注册
	:param request:
	:return:
	'''
	if request.method == 'POST':
		# form = SignInForm(request.POST)
		# if form.is_valid():  # 如果提交的数据合法
		username = request.POST.get('username', None)
		username = html.escape(username)
		password = request.POST.get('password', None)
		password = html.escape(password)
		sex = request.POST.get('sex', None)
		signature = request.POST.get('signature', None)
		signature = html.escape(signature)
		email = request.POST.get('email', None)
		email = html.escape(email)
		city = request.POST.get('city', None)
		birthday = request.POST.get('birthday', None)
		phone = request.POST.get('phone')
		users = User.objects.filter(username=username)
		if users.count() != 0:
			return JsonResponse({'code': -1, 'status': False, 'info': '注册失败, 用户名已经存在'})
		user = User.objects.create(username=username, password=password, email=email, phone=phone,
							city=city, birthday=birthday, signature=signature, sex=sex)
		# 用户创建成功的时候创建默认好友分组
		Group.objects.create(name="我的好友", owner=user)
		return JsonResponse({'code': 0, 'status': True, 'info': '注册成功', 'data': user.id})
		# return HttpResponseRedirect(reverse('index'))
	

def signup(request):
	'''
	跳往用户注册页面
	:param request:
	:return:
	'''
	return render(request, 'login/signup.html', {})


def logout(request):
	user_id = request.GET.get('user_id', None)
	if not user_id:
		return JsonResponse({'code': 0, 'msg': 'invalid user_id'})
	user = User.objects.get(pk=user_id)
	user.status = 'OFF'
	user.save()
	return render(request, 'login/login.html')