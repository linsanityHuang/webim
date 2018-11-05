from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from_email = settings.DEFAULT_FROM_EMAIL


def send():
	subject = '来自自强学堂的问候'
	
	text_content = '这是一封重要的邮件.'
	
	html_content = '<p>这是一封<strong>重要的</strong>邮件.</p>'
	
	msg = EmailMultiAlternatives(subject, text_content, from_email, ['528609844@qq.com'])
	
	msg.attach_alternative(html_content, "text/html")
	
	msg.send()