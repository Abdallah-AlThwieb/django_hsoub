import os
import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from blog.models import Post
from .models import Category, Course, Instructor, Lesson, Testimonial
from .forms import CommentForm, InstructorProfileForm
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def home_page(request):
    User = get_user_model()
    query = request.GET.get("q", "").strip()
    student_count = User.objects.annotate(course_count=Count('courses')).filter(course_count__gt=0).count()
    categories = Category.objects.annotate(course_count=Count('courses'))
    courses = Course.objects.filter(is_published=True)
    posts = Post.objects.order_by('-created_at')[:3]
    instructors = Instructor.objects.all()[:3]
    testimonials = Testimonial.objects.all()

    paginator = Paginator(courses, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'courses/home.html', {
        'student_count': student_count,
        'courses': courses,
        'posts': posts,
        'categories': categories,
        'categories': categories,
        'instructors': instructors,
        'testimonials': testimonials,
        'page_obj': page_obj,
        'query': query,
    })

def course_list(request):
    courses = Course.objects.filter(is_published=True)  
    query = request.GET.get("q", "").strip()
    sort_option = request.GET.get('sort')
    category = request.GET.get('category')
    level = request.GET.get('level')
    duration = request.GET.get('duration')
    price_filter = request.GET.get('price')

    paginator = Paginator(courses, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if category:
        courses = courses.filter(category__name=category)

    if level:
        courses = courses.filter(level__iexact=level)

    if duration:
        courses = courses.filter(duration__icontains=duration)

    if price_filter == 'free':
        courses = courses.filter(price=0)
    elif price_filter == 'paid':
        courses = courses.filter(price__gt=0)
        
    if query:
        courses = courses.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    
    if sort_option == 'newest':
        courses = courses.order_by('-created_at')
    elif sort_option == 'price_low':
        courses = courses.order_by('price')
    elif sort_option == 'price_high':
        courses = courses.order_by('-price')
    elif sort_option == 'duration':
        courses = courses.order_by('duration')
    elif sort_option == 'popular':
        courses = courses.annotate(student_count=Count('students')).order_by('-student_count')

    categories = Category.objects.all()
    levels = Course.objects.exclude(level__isnull=True).exclude(level__exact="").values_list('level', flat=True).distinct()
    durations = Course.objects.exclude(duration__isnull=True).exclude(duration__exact="").values_list('duration', flat=True).distinct()

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'categories': categories,
        'levels': levels,
        'durations': durations,
        'sort_option': sort_option,
        'page_obj': page_obj,
        })

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    is_enrolled = False
    if request.user.is_authenticated:
        if request.user.is_superuser:
            is_enrolled = True
        else:
            is_enrolled = course.students.filter(id=request.user.id).exists()

        if request.method == "POST":
            course.students.add(request.user)
            return redirect('courses:course_detail', course_id=course.id)

    discount = None
    if course.old_price and course.old_price > course.price:
        discount = int(round((1 - (course.price / course.old_price)) * 100))

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'discount': discount, 
    })

@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if not request.user.is_superuser and request.user not in lesson.course.students.all():
        messages.error(request, "يجب عليك شراء الدورة لمشاهدة محتوى الدرس.")
        return redirect("courses:course_detail", course_id=lesson.course.pk)

    comments = lesson.comments.all()
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.lesson = lesson
            comment.save()
            messages.success(request, "تم إضافة تعليقك بنجاح.")
            return redirect("courses:lesson_detail", pk=lesson.pk)

    return render(request, "courses/lesson_detail.html", {
        "lesson": lesson,
        "comments": comments,
        "comment_form": comment_form
    })

@login_required
def instructors_view(request):
    instructors = Instructor.objects.all()
    return render(request, 'courses/instructors.html', {'instructors': instructors})

@login_required
def instructor_profile(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'courses/instructor_profile.html', {
        'instructor': instructor
    })

@login_required
def edit_instructor_profile(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.user != instructor.user and not request.user.is_superuser:
        return HttpResponseForbidden("غير مسموح لك بتعديل هذا الملف")
    if request.method == 'POST':
        form = InstructorProfileForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('courses:instructor_profile', instructor_id=instructor.id)
        else:
            print(form.errors)
    else:
        form = InstructorProfileForm(instance=instructor)
    return render(request, 'courses/edit_profile.html', {'form': form})

@login_required
def create_checkout_session(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.user.email,
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': course.title,
                },
                'unit_amount': int(course.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        metadata={'course_id': str(course.id)},
        success_url=request.build_absolute_uri(f'/courses/{course.id}/success/'),
        cancel_url=request.build_absolute_uri(f'/courses/{course.id}/'),
    )
    return redirect(session.url, code=303)

@login_required
def course_payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.add(request.user)
    return render(request, "courses/payment_success.html", {"course": course})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')
        course_id = session['metadata'].get('course_id')

        try:
            course = Course.objects.get(id=course_id)
            user = User.objects.get(email=customer_email)
            course.students.add(user)
        except (Course.DoesNotExist, User.DoesNotExist):
            pass

    return HttpResponse(status=200)
    
@login_required
def my_courses(request):
    courses = request.user.courses.all() 
    return render(request, 'courses/my_courses.html', {'courses': courses})