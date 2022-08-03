from django.shortcuts import render
from django.conf import settings

DEBUG = False

def chat_home_screen(request):
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['room_id'] = "1"
	return render(request, "personal/home.html", context)


