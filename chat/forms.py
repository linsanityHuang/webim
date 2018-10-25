from django import forms


class UploadFileForm(forms.Form):
	file = forms.FileField()
	
	
class UploadImageForm(forms.Form):
	image = forms.ImageField()