import django
from django.db import models
import uuid
import datetime


class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=11)
	country = models.CharField(max_length=30, default='中国')
	province = models.CharField(max_length=30, default='北京')
	city = models.CharField(max_length=30, default='北京')
	# -1代表未知，0代表男性，1代表女性
	SEX = (
		(0, '男'),
		(1, '女'),
		(-1, '未知'),
	)
	sex = models.IntegerField(choices=SEX)
	birthday = models.DateField(default=django.utils.timezone.now)
	age = models.IntegerField(default=18)
	# 个性签名
	signature = models.TextField()
	# 用户头像
	avatar = models.CharField(max_length=128, default='/statics/img/default_avatar_male_180.gif')
	
	STATUS = (
		('ON', 'online'),
		('OFF', 'offline'),
	)
	status = models.CharField(max_length=8, choices=STATUS, default='OFF')
	# 群聊
	# group_chat = models.ManyToManyField('GroupChat', null=True, blank=True, verbose_name='群聊', on_delete=models.SET_NULL)

	def __str__(self):
		return self.username


class Group(models.Model):
	'''
	好友分组，属于某个用户
	一个用户（User）有多个好友分组（Group），
	一个好友分组（Group）只属于一个用户（User）
	'''
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', default=None)
	group_members = models.ManyToManyField(User)
	# , through = 'Membership', related_name = 'group_members'
	
	def __str__(self):
		return self.name


# class Membership(models.Model):
# 	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	group = models.ForeignKey(Group, on_delete=models.CASCADE)
# 	date_joined = models.DateField(default=django.utils.timezone.now)
#
# 	def __str__(self):
# 		return '<Membership: %s>' % self.group.name
	

class GroupChat(models.Model):
	'''
	群聊，独立于用户存在
	'''
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128)
	group_chat_avatar = models.CharField(max_length=128, default='/statics/img/default_avatar_male_180.gif')
	group_chat_members = models.ManyToManyField(User)	#, related_name='group_chat_members'
	
	def __str__(self):
		return self.name
	

# class GroupChatMembership(models.Model):
# 	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# 	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
# 	group_chat = models.ForeignKey(GroupChat, on_delete=models.SET_NULL, null=True)
	
	
class Message(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	from_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='msg_from_user')
	to_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='msg_to_user')
	# 0 文本; 1 图片; 2 视频; 3语音
	msg_type = models.IntegerField(default=0)
	content = models.CharField(max_length=255)
	

class ImageModel(models.Model):
	model_pic = models.ImageField(upload_to='statics/upload/%y%m%d', blank=True, null=True)
	
	
if __name__ == '__main__':
	ringo = User.objects.create(username="Ringo Starr")
	paul = User.objects.create(username="Paul McCartney")
	# beatles = Group.objects.create(name="The Beatles", owner=ringo)
	# m1 = Membership(user=ringo, group=beatles, date_joined=datetime.date(1962, 8, 16))
	# m1.save()
	# beatles.members.all()
	# ringo.group_set.all()
	# m2 = Membership.objects.create(user=paul, group=beatles, date_joined=datetime.date(1960, 8, 1))
	# beatles.members.all()
