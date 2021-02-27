from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import *

class CreateUserForm(UserCreationForm):
	username = forms.CharField(max_length=50)
	first_name = forms.CharField(required=True, max_length=50)
	last_name = forms.CharField(required=True, max_length=50)
	email = forms.EmailField(required=True, max_length=50)
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
	def clean(self):
		super(CreateUserForm, self).clean()
		username = self.cleaned_data.get('username')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if User.objects.filter(username=username).exists():
			self.errors['username'] = self.error_class(['Username is already taken.'])

		if password1 != password2:
			self.errors['password1'] = self.error_class(['Passwords do not match.'])

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['name','comment_text', 'stars']

