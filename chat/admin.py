from django.contrib import admin
from chat.models import User, GroupChat, Group, Message


admin.site.register(User)
admin.site.register(Group)
admin.site.register(GroupChat)
# admin.site.register(Membership)
# admin.site.register(Message)
# admin.site.register(GroupChatMembership)
