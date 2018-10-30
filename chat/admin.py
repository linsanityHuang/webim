from django.contrib import admin
from chat.models import User, GroupChat, Group, Message


class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username', 'sex', 'birthday', 'email', 'phone', 'status', 'signature')
	list_filter = ('sex', 'status', 'birthday')
	search_fields = ('username', 'phone')
	fieldsets = (
		(None, {
			'fields': (
				'name',
				('sex', 'birthday'),
				('email', 'phone'),
				'status',
			)
		}),
	)


admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(GroupChat)
# admin.site.register(Membership)
# admin.site.register(Message)
# admin.site.register(GroupChatMembership)
