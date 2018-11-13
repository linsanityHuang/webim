from django.contrib import admin
from chat.models import IMUser, IMGroupChat, IMGroup, Message


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


admin.site.register(IMUser, UserAdmin)
admin.site.register(IMGroup)
admin.site.register(IMGroupChat)
