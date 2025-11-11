from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name= models.CharField(max_length=150)
    def __str__(self):
        return self.name
    

class Post(models.Model):
    title= models.CharField(max_length=100)
    content= RichTextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)
    view_content = models.PositiveBigIntegerField(default=0)
    like_user = models.ManyToManyField(User, related_name= "like_post")


    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)