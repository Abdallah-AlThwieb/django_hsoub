from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("التصنيف"))

    def __str__(self):
        return self.name
    

class Instructor(models.Model):
    full_name = models.CharField(max_length=100, verbose_name=_("الاسم الكامل"))
    bio = models.TextField(blank=True, verbose_name=_("نبذة"))
    specialty = models.CharField(max_length=100, blank=True, verbose_name=_("التخصص"))
    photo = models.ImageField(upload_to='instructors/', blank=True, null=True, verbose_name=_("صورة المدرب"))
    email = models.EmailField(unique=True, verbose_name=_("البريد الإلكتروني"))
    rating = models.FloatField(default=0.0, verbose_name=_("التقييم"))
    facebook = models.URLField(blank=True, verbose_name=_("فيسبوك"))
    twitter = models.URLField(blank=True, verbose_name=_("تويتر"))
    linkedin = models.URLField(blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')

    def __str__(self):
        return self.full_name
    

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("عنوان الدورة"))
    description = models.TextField(verbose_name=_("وصف الدورة"))
    is_published = models.BooleanField(default=True, verbose_name=_("نشر الدورة"))
    price = models.DecimalField(max_digits=6, decimal_places=0, verbose_name=_("السعر"))
    old_price = models.DecimalField(max_digits=6, decimal_places=0, default=0, blank=True, verbose_name=_("السعر القديم"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))
    image = models.ImageField(upload_to='course_images/', null=True, blank=True, verbose_name=_("صورة الدورة"))
    duration = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("مدة الدورة"))
    level = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("مستوى الدورة"))
    prerequisites = models.TextField(blank=True, null=True, verbose_name=_("متطلبات الدورة"))
    
    students = models.ManyToManyField(User, related_name="courses", blank=True, verbose_name=_("الطلاب المشتركين"))
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("مدرب الدورة"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', null=True, blank=True, verbose_name=_("فئة الدورة"))

    class Meta:
        verbose_name = _("دورة")
        verbose_name_plural = _("الدورات")
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name=_("الدورة"))
    title = models.CharField(max_length=200, verbose_name=_("عنوان الدرس"))
    video = models.FileField(upload_to="lesson_videos/", blank=True, null=True, verbose_name=_("فيديو"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))

    class Meta:
        verbose_name = _("درس")
        verbose_name_plural = _("الدروس")
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("المستخدم"))
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="comments", verbose_name=_("الدرس"))
    content = models.TextField(verbose_name=_("التعليق"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ النشر"))

    class Meta:
        verbose_name = _("تعليق")
        verbose_name_plural = _("التعليقات")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
    

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="testimonials", null=True, blank=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    comment = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    source = models.CharField(max_length=100, blank=True) 

    def __str__(self):
        return f"{self.name} - {self.rating}★"
    
    @property
    def rating_int(self):
        return int(round(self.rating))