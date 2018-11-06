from django.shortcuts import render
from django.http import JsonResponse
from .models import Client
from django.views.decorators.csrf import csrf_exempt
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def agent(request):
	return render(request, 'agent/kefu.html')


@csrf_exempt
def create_user(request):
	client_id = request.POST.get('client_id', None)
	if client_id is None:
		return JsonResponse({'code': 1, 'msg': 'invalid client_id'})
	client = Client.objects.create(id=client_id)
	return JsonResponse({'code': 0, 'msg': '', 'data': {'username': client.name, 'id': client.id, 'avatar': client.avatar}})
