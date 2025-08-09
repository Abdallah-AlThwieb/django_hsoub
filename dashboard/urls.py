from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard_home, name='home'),

    # إدارة الدورات
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),

    # إدارة المقالات
    path('posts/', views.post_list, name='post_list'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/bulk-delete/', views.bulk_delete_posts, name='bulk_delete_posts'),
    path('posts/bulk-delete/confirm/', views.confirm_bulk_delete, name='confirm_bulk_delete'),

    # المدربون
    path('instructors/', views.instructor_list, name='instructor_list'),
    path('instructors/add/', views.add_instructor, name='add_instructor'),
    path('instructors/<int:instructor_id>/edit/', views.edit_instructor, name='edit_instructor'),
    path('instructors/<int:instructor_id>/delete/', views.delete_instructor, name='delete_instructor'),

    # التصنيفات
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
]