from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path('all-courses', views.course_list, name="course_list"),
    path('<int:course_id>/', views.course_detail, name="course_detail"),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('<int:course_id>/buy/', views.create_checkout_session, name='buy_course'),
    path('<int:course_id>/success/', views.course_payment_success, name='payment_success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('my-courses/', views.my_courses, name='my_courses'),
]