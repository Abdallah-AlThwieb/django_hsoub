import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hsoub_project.settings")

import django
django.setup()

import random
import requests
from faker import Faker
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from courses.models import Category, Course, Lesson, Instructor
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import IntegrityError, transaction

User = get_user_model()

# بيانات ثابتة للمدربين (٦ مدربين رجال)
instructors_data = [
    {
    "full_name": "فهد العبدالله",
    "bio": "خبير في تطوير تطبيقات الموبايل باستخدام Flutter و React Native.",
    "specialty": "تطوير تطبيقات الموبايل",
    "email": "fahd.abdallah@example.com",
    "rating": 4.8,
    "facebook": "https://facebook.com/fahd.abdallah",
    "twitter": "",
    "linkedin": "https://linkedin.com/in/fahd.abdallah"
},
{
    "full_name": "مازن الشريف",
    "bio": "محاضر في هندسة البرمجيات وأنظمة المعلومات، بخبرة أكاديمية وعملية.",
    "specialty": "هندسة البرمجيات",
    "email": "mazen.shareef@example.com",
    "rating": 4.6,
    "facebook": "",
    "twitter": "https://twitter.com/mazen.shareef",
    "linkedin": ""
},
{
    "full_name": "يوسف داوود",
    "bio": "مدرب في مجال الحوسبة السحابية والبنى التحتية الرقمية.",
    "specialty": "الحوسبة السحابية",
    "email": "yousef.dawood@example.com",
    "rating": 4.7,
    "facebook": "",
    "twitter": "",
    "linkedin": "https://linkedin.com/in/yousef.dawood"
}
]

created_instructors = 0

for data in instructors_data:
    # تحقق من وجود مستخدم بنفس البريد الإلكتروني
    if Instructor.objects.filter(email=data["email"]).exists():
        print(f"⚠️ Skipping duplicate instructor '{data['full_name']}'")
        continue

    # إنشاء مستخدم مرتبط بالمدرب
    user, created = User.objects.get_or_create(
        username=data["email"],
        defaults={"email": data["email"]}
    )
    if created:
        user.set_password("abdallah")
        user.save()

    instructor = Instructor(
        full_name=data["full_name"],
        bio=data["bio"],
        specialty=data["specialty"],
        email=data["email"],
        rating=data["rating"],
        facebook=data["facebook"],
        twitter=data["twitter"],
        linkedin=data["linkedin"],
        user=user
    )

    try:
        with transaction.atomic():
            instructor.save()
        created_instructors += 1
        print(f"✅ Created instructor: {data['full_name']}")
    except IntegrityError as e:
        print(f"⚠️ Skipping duplicate instructor '{data['full_name']}': {e}")
    except Exception as e:
        print(f"❌ Error creating instructor '{data['full_name']}': {e}")

print(f"\n✅ تم إنشاء {created_instructors} مدربين بنجاح.")