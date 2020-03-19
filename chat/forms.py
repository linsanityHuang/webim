from django import forms
from .models import IMUser


class SignUpForm(forms.Form):
	class Meta:
		model = IMUser
		fields = (
			'username', 'password', 'email',
			'phone', 'sex', 'birthday'
		)


class UploadFileForm(forms.Form):
	file = forms.FileField()
	
	
class UploadImageForm(forms.Form):
	image = forms.ImageField()
