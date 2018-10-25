from django import forms


class SignInForm(forms.Form):
	username = forms.CharField
	password = forms.CharField
	password_again = forms.CharField
	sex = forms.CharField
	signature = forms.CharField
	email = forms.CharField
	city = forms.CharField
	birthday = forms.CharField
	phone = forms.CharField


class LoginForm(forms.Form):
	username = forms.CharField
	password = forms.CharField
