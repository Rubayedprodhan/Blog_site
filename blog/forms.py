from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
class Post_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tag']

class Comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class Update_Profile_forms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form_control'}),
            'first_name' : forms.TextInput(attrs={'class':'form_control'}),
            'last_name' :forms.TextInput(attrs={'class':'form_control'}),
            'email' : forms.EmailInput(attrs={'class':'form_control'})
        }
