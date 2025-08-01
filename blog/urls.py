from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    re_path(r'^(?P<slug>[\w\u0600-\u06FF-]+)/$', views.blog_detail, name='blog_detail'),
]