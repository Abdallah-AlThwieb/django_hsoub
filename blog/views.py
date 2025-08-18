from django.shortcuts import redirect, render, get_object_or_404
from blog.forms import PostCommentForm
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
    comments = post.comments.all()
    error = None

    form = PostCommentForm()  # تعريف الفورم مسبقًا

    if request.method == "POST":
        if request.user.is_authenticated:
            form = PostCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect("blog:blog_detail", slug=slug)
        else:
            error = "يجب تسجيل الدخول لنشر التعليق."

    return render(request, "blog/blog_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
        "error": error,
    })