from django import forms
from courses.models import Course, Instructor, Lesson, Category, User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم التصنيف'}),
        }


class InstructorForm(forms.ModelForm):
    username = forms.CharField(label="اسم المستخدم")
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput)

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['username'].required = False
            self.fields['password'].required = False

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if self.instance and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise forms.ValidationError("اسم المستخدم موجود بالفعل.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs_instructor = Instructor.objects.filter(email=email)
        if self.instance:
            qs_instructor = qs_instructor.exclude(pk=self.instance.pk)
        if qs_instructor.exists():
            raise forms.ValidationError("البريد الإلكتروني مستخدم بالفعل لمدرب آخر.")
        qs_user = User.objects.filter(email=email)
        if self.instance and self.instance.user:
            qs_user = qs_user.exclude(pk=self.instance.user.pk)
        if qs_user.exists():
            raise forms.ValidationError("البريد الإلكتروني مستخدم بالفعل لحساب مستخدم آخر.")
        return email
        

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