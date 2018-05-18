from django import forms

from BioWeb.models import *
class UserForm(forms.ModelForm):
	name=forms.CharField(label='姓名',required=True)
	passwd=forms.CharField(label='密码',widget=forms.PasswordInput(),required=True)
	class Meta:
		model=User
		fields=('name','passwd')	
'''
class FileForm(forms.ModelForm):
	name=forms.CharField(label='文件名',required=True)
	passwd=forms.CharField(label='路径',widget=forms.PasswordInput(),required=True)
	class Meta:
		model=Update_file
		fields=('name','path')
'''
class UpdateForm(forms.Form):
	DNA=forms.CharField()
	myfile=forms.FileField()





