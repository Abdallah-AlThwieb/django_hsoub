from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from courses.models import Category, Course, Instructor, User
from .forms import CategoryForm, CourseForm, InstructorForm, LessonFormSet
from blog.models import Post
from blog.forms import PostForm 
from django.contrib import messages

# Create your views here.
def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def dashboard_home(request):
    return render(request, 'dashboard/dashboard_home.html')

@user_passes_test(is_admin)
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'dashboard/course/course_list.html', {'courses': courses})

@user_passes_test(is_admin)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        formset = LessonFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            course = form.save()
            lessons = formset.save(commit=False)
            for lesson in lessons:
                lesson.course = course
                lesson.save()
            return redirect('dashboard:course_list')
    else:
        form = CourseForm()
        formset = LessonFormSet()

    return render(request, 'dashboard/course/add_course.html', {'form': form, 'formset': formset})

@user_passes_test(is_admin)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        formset = LessonFormSet(request.POST, request.FILES, instance=course)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dashboard:course_list')
    else:
        form = CourseForm(instance=course)
        formset = LessonFormSet(instance=course)
    return render(request, 'dashboard/course/edit_course.html', {'form': form, 'formset': formset, 'course': course})

@user_passes_test(is_admin)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        messages.success(request, "تم حذف الدورة.")
        return redirect('dashboard:course_list')
    return render(request, "dashboard/course/confirm_delete_course.html", {"course": course})

@user_passes_test(is_admin)
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES) 
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "تمت إضافة المقالة بنجاح.")
            return redirect("dashboard:post_list")
    else:
        form = PostForm()
    return render(request, "dashboard/blog/add_post.html", {"form": form})

@user_passes_test(is_admin)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, request.FILES, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "تم تعديل المقالة بنجاح.")
        return redirect("dashboard:post_list")
    return render(request, "dashboard/blog/edit_post.html", {"form": form, "post": post})

@user_passes_test(is_admin)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        messages.success(request, "تم حذف المقالة.")
        return redirect("dashboard:post_list")
    return render(request, "dashboard/blog/delete_post.html", {"post": post})

@user_passes_test(is_admin)
def bulk_delete_posts(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_posts')
        if ids:
            Post.objects.filter(id__in=ids).delete()
            messages.success(request, f"تم حذف {len(ids)} مقالة.")
        else:
            messages.warning(request, "لم يتم تحديد أي مقالة.")
    return redirect('dashboard:confirm_bulk_delete') 

@user_passes_test(is_admin)
def confirm_bulk_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_posts')
        posts = Post.objects.filter(id__in=ids)
        return render(request, 'dashboard/blog/confirm_bulk_delete.html', {'posts': posts})
    return redirect('dashboard:post_list')

@user_passes_test(is_admin)
def post_list(request):
    posts = Post.objects.all()
    return render(request, "dashboard/blog/post_list.html", {"posts": posts})

@user_passes_test(is_admin)
def instructor_list(request):
    instructors = Instructor.objects.all()
    return render(request, 'dashboard/instructor/instructor_list.html', {'instructors': instructors})

@user_passes_test(is_admin)
def add_instructor(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, password=password)

            instructor = form.save(commit=False)
            instructor.user = user
            instructor.save()
            return redirect('dashboard:instructor_list')
    else:
        form = InstructorForm()
    return render(request, 'dashboard/instructor/instructor_form.html', {'form': form, 'title': 'إضافة مدرب'})

@user_passes_test(is_admin)
def edit_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.method == 'POST':
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل بيانات المدرب بنجاح.")
            return redirect('dashboard:instructor_list')
    else:
        form = InstructorForm(instance=instructor)
    return render(request, 'dashboard/instructor/instructor_form.html', {'form': form, 'title': 'تعديل بيانات مدرب'})

@user_passes_test(is_admin)
def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.method == "POST":
        instructor.delete()
        messages.success(request, "تم حذف المدرب.")
        return redirect("dashboard:instructor_list")
    return render(request, "dashboard/instructor/delete_instructor.html", {"instructor": instructor})

@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category/category_list.html', {'categories': categories})

@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category/category_form.html', {'form': form, 'title': 'إضافة تصنيف'})

@user_passes_test(is_admin)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل بيانات التصنيف بنجاح.")
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category/category_form.html', {'form': form, 'title': 'تعديل التصنيف'})

@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.delete()
        messages.success(request, "تم حذف التصنيف.")
        return redirect("dashboard:category_list")
    return render(request, "dashboard/category/delete_category.html", {"category": category})