import uuid
import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class IMUser(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	username = models.CharField(max_length=100, unique=True, verbose_name="用户名")
	password = models.CharField(max_length=100, verbose_name="密码")
	email = models.EmailField(verbose_name="邮箱")
	phone = models.CharField(max_length=11, verbose_name="手机号")
	country = models.CharField(max_length=30, default='中国', verbose_name="国家")
	province = models.CharField(max_length=30, default='北京', verbose_name="省份")
	city = models.CharField(max_length=30, default='北京', verbose_name="城市")
	# -1代表未知，0代表男性，1代表女性
	SEX = (
		(0, '男'),
		(1, '女'),
		(-1, '未知'),
	)
	sex = models.IntegerField(choices=SEX, verbose_name="性别")
	birthday = models.DateField(default=django.utils.timezone.now, verbose_name="生日")
	age = models.IntegerField(default=18, verbose_name="年龄")
	# 个性签名
	signature = models.TextField(null=True, default="这个人懒得没有签名...", verbose_name="个性签名")
	# 用户头像
	avatar = models.CharField(max_length=128, default='/statics/img/default_avatar_male_180.gif', verbose_name="头像")
	
	STATUS = (
		('ON', 'online'),
		('OFF', 'hide'),
	)
	status = models.CharField(max_length=8, choices=STATUS, default='OFF', verbose_name="状态")
	created_time = models.DateTimeField(editable=False, default=now, verbose_name="创建时间")
	
	def __str__(self):
		return self.username


class IMGroup(models.Model):
	'''
	好友分组，属于某个用户
	一个用户（User）有多个好友分组（Group），
	一个好友分组（Group）只属于一个用户（User）
	'''
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128)
	owner = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='owner', default=None)
	group_members = models.ManyToManyField(IMUser, related_name='group_members')
	
	def __str__(self):
		return self.name
	

class IMGroupChat(models.Model):
	'''
	群聊，独立于用户存在
	'''
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128)
	# 群聊管理员
	group_admins = models.ManyToManyField(IMUser, related_name="im_group_admins")
	group_chat_avatar = models.CharField(max_length=128, default='/statics/img/default_avatar_male_180.gif')
	group_chat_members = models.ManyToManyField(IMUser, related_name='im_group_chat_members')
	
	def __str__(self):
		return self.name

	
class Message(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	from_user_id = models.CharField(max_length=255)
	from_user_name = models.CharField(max_length=255)
	from_user_avatar = models.CharField(max_length=255)
	to_user_or_group_id = models.CharField(max_length=255)
	# from_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='msg_from_user')
	# to_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='msg_to_user')
	# 消息来自私聊还是群聊
	# friend 私聊 group 群聊
	channel_type = models.CharField(max_length=32, default='friend')
	# 0 文本; 1 图片; 2 视频; 3语音
	msg_type = models.IntegerField(default=0)
	content = models.CharField(max_length=255)
	timestamp = models.BigIntegerField()
	

class ImageModel(models.Model):
	model_pic = models.ImageField(upload_to='statics/upload/%y%m%d', blank=True, null=True)
	

class FileModel(models.Model):
	model_file = models.FileField(upload_to='statics/upload/%y%m%d', blank=True, null=True)

