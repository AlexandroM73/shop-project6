from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'preview_image', 'is_published']
        # created_at и views_count управляются автоматически, поэтому их нет в форме
