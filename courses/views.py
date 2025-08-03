import os
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Course, Lesson, Comment
from .forms import CommentForm
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def home_page(request):
    User = get_user_model()
    student_count = User.objects.annotate(course_count=Count('courses')).filter(course_count__gt=0).count()
    courses = Course.objects.filter(status='Posted')

    return render(request, 'courses/home.html', {
        'student_count': student_count,
        'courses': courses,
    })

def course_list(request):
    courses = Course.objects.filter(status='Posted')  
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_superuser:
        is_enrolled = True
    else:
        is_enrolled = course.students.filter(id=request.user.id).exists()

    if request.method == "POST":
        course.students.add(request.user)
        return redirect('courses:course_detail', course_id=course.id)

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
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