from django.shortcuts import render, redirect, reverse,render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from chat.models import User
from django.contrib.auth import authenticate, login, logout


def do_login(request):
	'''
	执行登录逻辑，登录成功跳往聊天界面
	:param request:
	:return:
	'''
	if request.method == 'GET':
		return render(request, 'login.html')
	
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)
	print('username', username)
	print('password', password)
	# user = authenticate(request, username=username, password=password)
	user = User.objects.get(username=username, password=password)
	print(user)
	print(1)
	if user is not None:
		# 查询好友，群组，历史记录
		# login(request, user)
		print('已登录')
		return JsonResponse({'code': 0, 'status': True, 'info': '登录成功', 'user_id': user.id})
	else:
		print(2)
		return render(request, 'login.html', {
			'username': username,
			'password': password,
		})


def signin(request):
	'''
	用户注册
	:param request:
	:return:
	'''
	print('用户注册')
	print(request)
	print(request.method)
	print(request.POST)
	if request.method == 'POST':
		# form = SignInForm(request.POST)
		# if form.is_valid():  # 如果提交的数据合法
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		sex = request.POST.get('sex', None)
		signature = request.POST.get('signature', None)
		email = request.POST.get('email', None)
		city = request.POST.get('city', None)
		birthday = request.POST.get('birthday', None)
		phone = request.POST.get('phone')
		print('username', username)
		print('password', password)
		print('sex', sex)
		print('signature', signature)
		print('email', email)
		print('city', city)
		print('birthday', birthday)
		print('phone', phone)
		user = User.objects.filter(username=username)
		print(user)
		if len(user) == 1:
			return JsonResponse({'code': -1, 'status': False, 'info': '注册失败, 用户名已经存在'})
		user = User.objects.create(username=username, password=password, email=email, phone=phone,
							city=city, birthday=birthday, signature=signature, sex=sex)
		return JsonResponse({'code': 0, 'status': True, 'info': '注册成功', 'data': user.id})
	

def signup(request):
	'''
	跳往用户注册页面
	:param request:
	:return:
	'''
	return render(request, 'signup.html', {})


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))