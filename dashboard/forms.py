from django import forms
from courses.models import Course, Instructor, Lesson, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم التصنيف'}),
        }


class InstructorForm(forms.ModelForm):
    username = forms.CharField(label="اسم المستخدم")
    password = forms.CharField(label="كلمة المرور")

    class Meta:
        model = Instructor
        fields = [
            'full_name', 'bio', 'specialty', 'photo', 'email', 
            'rating', 'facebook', 'twitter', 'linkedin', 'username', 'password'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الكامل'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'نبذة عن المدرب'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'التخصص'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط فيسبوك'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط تويتر'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط لينكدإن'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المستخدم'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'أدخل كلمة المرور'})
        }
        

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'price', 'is_published',
            'instructor', 'category',  
            'image', 'duration', 'level', 'prerequisites'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'instructor': forms.Select(attrs={'class': 'form-select'}),  
            'category': forms.Select(attrs={'class': 'form-select'}),    
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.TextInput(attrs={'class': 'form-control'}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

LessonFormSet = forms.inlineformset_factory(
    Course, Lesson, form=LessonForm,
    extra=1, can_delete=True
)