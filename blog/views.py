from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils.translation import gettext as _
from django.core.paginator import Paginator

# Create your views here.
def blog_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')

    paginator = Paginator(posts, 5) 
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'posts_page': posts_page,
        })


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'blog/blog_detail.html', {'post': post})