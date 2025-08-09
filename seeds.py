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
from django.db import IntegrityError, transaction

fake = Faker('ar_JO')

# عدد المقالات
NUM_ARTICLES = 30

User = get_user_model()
# حاول إيجاد مشرف أولًا، ثم أي مستخدم، وإذا لم يوجد حاول إنشاء مستخدم بسيط
author = User.objects.filter(is_superuser=True).first()
if not author:
    author = User.objects.filter(is_staff=True).first()
if not author:
    author = User.objects.first()

if not author:
    try:
        # نحاول إنشاء مستخدم بسيط كحل احتياطي (قد يختلف توقيع create_user حسب موديل المستخدم لديك)
        author = User.objects.create_user(username='seed_admin', email='seed@example.com', password='password')
        print("Created seed user 'seed_admin' with password 'password'. Please change credentials if needed.")
    except Exception as e:
        raise RuntimeError(
            "لم يتم العثور على أي مستخدم في قاعدة البيانات، وفشل إنشاء مستخدم احتياطي أوتوماتيكيًا. "
            "يرجى إنشاء مستخدم/مشرف يدويًا قبل تشغيل seeds.py."
        ) from e

titles = [
    "أهمية تعلم البرمجة للأطفال",
    "كيف يؤثر الذكاء الاصطناعي على التعليم",
    "أسباب نجاح التعليم عبر الإنترنت",
    "أفضل طرق تنظيم الوقت أثناء الدراسة",
    "لماذا يعتبر التعلم الذاتي مهمًا في العصر الحديث",
    "كيف تبدأ تعلم تطوير الويب من الصفر",
    "أهمية اللغة الإنجليزية في سوق العمل",
    "أهم المهارات المطلوبة في عام 2025",
    "كيفية الاستعداد للامتحانات بكفاءة",
    "العلاقة بين النوم الجيد والتحصيل الدراسي",
    "أثر التكنولوجيا على العملية التعليمية",
    "مستقبل الوظائف في ظل الأتمتة",
    "كيف تبني خطة دراسية فعالة",
    "تأثير الألعاب التعليمية على الأطفال",
    "دور المعلم في العصر الرقمي",
    "مقارنة بين التعليم التقليدي والتعليم الإلكتروني",
    "كيفية تحسين مهاراتك في التفكير النقدي",
    "خطوات البدء في تعلم الذكاء الاصطناعي",
    "أهمية تعلم لغة ثانية",
    "نصائح للنجاح في التعلم الذاتي",
    "أشهر مجالات العمل الحر في العالم الرقمي",
    "كيف تختار تخصصك الجامعي المناسب",
    "أثر القراءة اليومية على تنمية العقل",
    "أفضل تطبيقات لتنظيم الوقت والمذاكرة",
    "ما الفرق بين التعلم النشط والتقليدي؟",
    "فوائد تعلم التصميم الجرافيكي",
    "طرق فعالة لتطوير مهارات الكتابة الأكاديمية",
    "مميزات استخدام الفيديوهات التعليمية",
    "لماذا يفشل الطلاب في تنظيم وقتهم؟",
    "كيف تصبح متعلمًا مدى الحياة؟",
]

IMAGE_DIR = os.path.join("media", "blog")
os.makedirs(IMAGE_DIR, exist_ok=True)

paragraphs = [
    "في ظل التطور السريع للتكنولوجيا، أصبح من الضروري مواكبة المهارات الرقمية لضمان التنافسية في سوق العمل.",
    "يعتمد النجاح في التعلم الذاتي على وجود خطة واضحة وجدول زمني منظم يلتزم به المتعلم.",
    "القراءة اليومية حتى لو لوقت قصير تعزز من الفهم وتنمّي القدرة على التحليل والنقد.",
    "توفر منصات التعليم المفتوح موارد غنية ومتنوعة يمكن الاستفادة منها في أي وقت ومن أي مكان.",
    "الذكاء الاصطناعي أصبح يلعب دورًا مهمًا في تطوير وسائل التعليم وتقديم محتوى مخصص لكل متعلم.",
    "تساعد بيئة التعلم التفاعلية في رفع مستوى التحفيز وزيادة معدلات التعلّم مقارنة بالطرق التقليدية.",
    "اللغة الإنجليزية تُعد من المهارات الأساسية التي تفتح أبوابًا واسعة للفرص العالمية.",
    "من المهم تقييم التقدم في التعلم الذاتي بشكل دوري لتحديد نقاط القوة والعمل على التحسين.",
    "الدورات المصغّرة عبر الإنترنت (Microlearning) تعتبر وسيلة فعالة لتعلم المفاهيم بسرعة.",
    "يجب على المتعلم أن يتحلى بروح المبادرة وأن يبحث عن الإجابات بنفسه قبل طلب المساعدة.",
    "أصبح بإمكان الجميع الآن الوصول إلى دورات من جامعات عالمية دون الحاجة للسفر.",
    "الاستذكار الفعّال يعتمد على التكرار المنظم واستخدام الخرائط الذهنية وأساليب التلخيص.",
    "تشجيع الأطفال على البرمجة في سن مبكرة ينمّي قدراتهم التحليلية وحل المشكلات.",
    "تعلُّم مهارة جديدة قد يفتح لك آفاقًا لم تتخيلها سواء في العمل أو في الحياة الشخصية.",
    "يساعدك تحديد أهداف أسبوعية على الالتزام بخطة التعلم وتقليل الشعور بالإرهاق.",
    "التغذية السليمة والنوم الجيد لهما أثر مباشر على التركيز والانتباه خلال التعلم.",
    "التعلم من الأخطاء عنصر أساسي في أي تجربة تعليمية ناجحة، ولا يجب الخوف من الفشل.",
    "استخدام وسائل مرئية مثل الفيديوهات والمخططات يساعد في ترسيخ المعلومات.",
    "تدوين الملاحظات أثناء التعلم يعزز من الفهم ويساعد على تذكّر المعلومات لاحقًا.",
    "يمكن للمتعلمين التعاون ضمن مجموعات عبر الإنترنت لتعزيز الفهم وتحقيق نتائج أفضل.",
    "من الجيد تخصيص مكان هادئ ومريح للدراسة بعيدًا عن المشتتات والضوضاء.",
    "ربط المعلومات الجديدة بمعرفة سابقة يسهل حفظها واستدعاءها لاحقًا.",
    "تعلم لغة برمجة واحدة يمكن أن يفتح لك المجال لفهم باقي اللغات بسهولة.",
    "قد لا تكون السرعة في التعلم مهمة بقدر الاستمرارية والالتزام على المدى الطويل.",
    "الاهتمام بالجانب العملي أثناء التعلم يزيد من التفاعل والفهم العميق.",
    "تحديد دوافعك الشخصية للتعلم يساعدك على الحفاظ على الحافز لفترة أطول.",
    "استخدام تطبيقات الجدولة والتذكير يساعد على تنظيم المهام الدراسية اليومية.",
    "قراءة تجارب الناجحين في مجالات مختلفة يمكن أن تلهمك وتوجهك في طريقك.",
    "المشاركة في المنتديات التعليمية والنقاشات يزيد من استيعاب المفاهيم بعمق.",
    "التقييم الذاتي بعد كل فترة تعلم يمنحك رؤية أوضح لمستواك ويحفزك على التقدم."
]

def get_unique_slug(model, base_text):
    """
    يرجع slug فريد مبنيًا على base_text.
    إذا كان الـ slug موجودًا بالفعل في الجدول، يضيف عدادًا (-1, -2, ...) حتى يصبح فريدًا.
    """
    base_slug = slugify(base_text)
    if not base_slug:
        # في حال slugify أعاد سلسلة فارغة (نادر) نستخدم timestamp كقاعدة
        base_slug = slugify(str(timezone.now().timestamp()))
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

created_count = 0

for i in range(NUM_ARTICLES):
    title = random.choice(titles)
    # نستخدم العنوان كأساس للـ slug (الدالة ستجعلها فريدة إذا لزم)
    slug = get_unique_slug(Post, title)

    content = "\n\n".join(random.sample(paragraphs, k=5))
    created_at = timezone.now() - timedelta(days=random.randint(1, 365))

    image_url = f"https://picsum.photos/800/400?random={random.randint(1, 10000)}"
    try:
        response = requests.get(image_url, timeout=10)
    except Exception as e:
        response = None
        print(f"Warning: failed to download image for '{title}': {e}")

    image_name = f"seed_{slug}_{i}.jpg"

    post = Post(
        title=title,
        slug=slug,
        content=content,
        author=author,
        created_at=created_at,
        updated_at=created_at,
        is_published=True
    )

    if response and getattr(response, "status_code", None) == 200:
        try:
            post.image.save(image_name, ContentFile(response.content), save=False)
        except Exception as e:
            print(f"Warning: failed to attach image for post '{title}': {e}")

    try:
        with transaction.atomic():
            post.save()
        created_count += 1
        print(f"Created post: {title} ({slug})")
    except IntegrityError as e:
        # هذا يجب أن يتجنّب تكرار الـ slug، لكنه يبقى احتاطيًا
        print(f"Skipping duplicate (IntegrityError) for '{title}' slug='{slug}': {e}")
    except Exception as e:
        print(f"Error creating post '{title}': {e}")

print(f"✅ تم إنشاء {created_count} من أصل {NUM_ARTICLES} مقالات بنجاح.")
