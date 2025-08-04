from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Comment, Course, Lesson
from django.forms import inlineformset_factory


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label=_("أضف تعليقك"),
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
    )

    class Meta:
        model = Comment
        fields = ['content']
        

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'is_published','duration', 'level', 'prerequisites']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video']


LessonFormSet = inlineformset_factory(
    Course, Lesson, form=LessonForm,
    extra=1, 
    can_delete=True 
)