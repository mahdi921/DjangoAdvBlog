from django import forms
from blog.models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = [ 'title', 'content', 'category', 'status',  'published_date']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'