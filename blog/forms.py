from django import forms
from .models import Post
from courses.models import Comment
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'is_published']
        labels = {
            'title': _('عنوان المقالة'),
            'content': _('المحتوى'),
            'image': _('صورة المقال'),
            'is_published': _('نشر المقالة'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['user', 'content'] 
        widgets = {
            'content': forms.Textarea(attrs={'rows':4, 'class':'form-control', 'placeholder':'اكتب تعليقك هنا'}),
            'user': forms.TextInput(attrs={'class':'form-control', 'placeholder':'الاسم'}),
        }