from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Course, Lesson, Comment, Instructor, Testimonial


admin.site.register(Instructor)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_at", "is_published")
    list_display_links = ("title",)
    list_editable = ("price",)
    search_fields = ("title",)
    list_filter = ("created_at", "is_published")

    def get_queryset(self, request):
        return super().get_queryset(request)

    def title(self, obj):
        return obj.title
    title.short_description = _("عنوان الدورة")

    def price(self, obj):
        return obj.price
    price.short_description = _("السعر")

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = _("تاريخ الإنشاء")

    def is_published(self, obj):
        return obj.is_published
    is_published.short_description = _("منشورة")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "created_at")
    list_display_links = ("title",)
    search_fields = ("title", "course__title")
    list_filter = ("course", "created_at")

    def title(self, obj):
        return obj.title
    title.short_description = _("عنوان الدرس")

    def course(self, obj):
        return obj.course
    course.short_description = _("الدورة")

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = _("تاريخ الإنشاء")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "created_at")
    list_display_links = ("user", "lesson")
    search_fields = ("user__username", "lesson__title")
    list_filter = ("created_at", "lesson")

    def user(self, obj):
        return obj.user
    user.short_description = _("المستخدم")

    def lesson(self, obj):
        return obj.lesson
    lesson.short_description = _("الدرس")

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = _("تاريخ النشر")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'source')
    search_fields = ('name', 'role', 'source')