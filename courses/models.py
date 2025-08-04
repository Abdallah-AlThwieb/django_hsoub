from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("عنوان الدورة"))
    description = models.TextField(verbose_name=_("وصف الدورة"))
    is_published = models.BooleanField(default=True, verbose_name=_("نشر الدورة"))
    price = models.DecimalField(max_digits=6, decimal_places=0, verbose_name=_("السعر"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))
    students = models.ManyToManyField(User, related_name="courses", blank=True, verbose_name=_("الطلاب المشتركين"))
    image = models.ImageField(upload_to='course_images/', null=True, blank=True, verbose_name=_("صورة الدورة"))
    duration = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("مدة الدورة"))
    level = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("مستوى الدورة"))
    prerequisites = models.TextField(blank=True, null=True, verbose_name=_("متطلبات الدورة"))
    
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