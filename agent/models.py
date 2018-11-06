import uuid
from django.db import models


class Agent(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=100, verbose_name="客服名称")
	password = models.CharField(max_length=100, verbose_name="密码")
	# 客服头像
	avatar = models.CharField(max_length=128, default='/statics/img/default_avatar_male_180.gif', verbose_name="客服头像")


class Client(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=100, verbose_name="客户昵称", default='访客')
	# 客户头像
	avatar = models.CharField(max_length=128, default='/statics/img/default_avatar_male_180.gif', verbose_name="客户头像")
	# 客户的IP地址
	ip = models.CharField(max_length=64, default='0.0.0.0', verbose_name='客户IP')


class Dialogue(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128, verbose_name='对话名称')
	agent = models.ForeignKey('Agent', on_delete=models.CASCADE, null=True, related_name='agent')
	client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, related_name='client')


class Statement(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	dialogue = models.ForeignKey('Dialogue', on_delete=models.CASCADE, null=True, related_name='dialogue')
	from_id = models.CharField(max_length=255)
	# from_user_name = models.CharField(max_length=255)
	# from_user_avatar = models.CharField(max_length=255)
	to_id = models.CharField(max_length=255)
	# from_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='msg_from_user')
	# to_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='msg_to_user')
	# 0 文本; 1 图片; 2 视频; 3语音
	msg_type = models.IntegerField(default=0)
	content = models.CharField(max_length=255)
	timestamp = models.BigIntegerField()