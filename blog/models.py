from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("عنوان المقال"))
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, verbose_name=_("الرابط"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("الكاتب"))
    content = models.TextField(verbose_name=_("محتوى المقال"))
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True, verbose_name=_("صورة المقال"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ النشر"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخر تحديث"))
    is_published = models.BooleanField(default=True, verbose_name=_("منشور"))

    class Meta:
        verbose_name = _("مقال")
        verbose_name_plural = _("مقالات")
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)