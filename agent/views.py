from django.shortcuts import render


def agent(request):
	return render(request, 'agent/kefu.html')