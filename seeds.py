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
from blog.models import Post 
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

fake = Faker('ar_EG')

# عدد المقالات
NUM_ARTICLES = 50

User = get_user_model()
author = User.objects.filter(is_superuser=True).first()

IMAGE_DIR = os.path.join("media", "blog")
os.makedirs(IMAGE_DIR, exist_ok=True)

for i in range(NUM_ARTICLES):
    title = fake.sentence(nb_words=6)
    slug = slugify(title)
    content = fake.paragraph(nb_sentences=30)
    created_at = timezone.now() - timedelta(days=random.randint(1, 365))
    image_url = f"https://picsum.photos/800/400?random={random.randint(1, 10000)}"
    response = requests.get(image_url)
    image_name = f"seed_{slug}_{i}.jpg"

    # إنشاء المقال
    post = Post(
        title=title,
        slug=slug,
        content=content,
        author=author,
        created_at=created_at,
        updated_at=created_at,
        is_published=True
    )

    if response.status_code == 200:
        post.image.save(image_name, ContentFile(response.content), save=False)

    post.save()

print(f"✅ تم إنشاء {NUM_ARTICLES} مقالات بصور بنجاح.")
