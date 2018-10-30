from django import forms
from .models import User


class SignUpForm(forms.Form):
	class Meta:
		model = User
		fields = (
			'username', 'password', 'email',
			'phone', 'sex', 'birthday'
		)


class UploadFileForm(forms.Form):
	file = forms.FileField()
	
	
class UploadImageForm(forms.Form):
	image = forms.ImageField()