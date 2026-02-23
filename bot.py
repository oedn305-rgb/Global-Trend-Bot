import os
import random
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# 1. إعدادات الجيمني (Gemini Config)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash') # أحدث موديل متاح حالياً

# 2. إعدادات بلوجر (Blogger Config)
BLOG_ID = "YOUR_BLOG_ID"

# 3. الكلمات المفتاحية لجلب الترند (عربي + English)
keywords = [
    "AI breakthroughs 2026", "Global Economy Trends", "Future Technology", 
    "أحدث تقنيات الذكاء الاصطناعي", "أخبار الفضاء والعلوم", "ترند الرياضة العالمية",
    "Sustainable Energy News", "أخبار التكنولوجيا المالية", "World Innovation"
]

def generate_article(topic):
    prompt = (
        f"Write a comprehensive professional article about '{topic}'.\n"
        "The response must be in HTML format and include two sections:\n"
        "1. Arabic Section: Starts with <h1> title, followed by an introduction, <h2> subheadings, and a detailed body.\n"
        "2. English Section: A complete professional English translation of the same article below the Arabic part.\n"
        "Use 💡, 🚀, 🌍 emojis. Make it SEO friendly. Wrap the Arabic part in <div dir='rtl'> and the English in <div dir='ltr'>."
    )
    
    response = model.generate_content(prompt)
    return response.text

def post_to_blogger(title, content):
    # هنا يتم استدعاء ملف الاعتماد (credentials.json) الذي قمت برفعه على GitHub Secrets
    # تأكد من أنك قمت بإعداد OAuth2 بشكل صحيح في مشروعك
    try:
        # ملاحظة: هذا الجزء يفترض وجود توكن أو صلاحية وصول مسبقة
        # للنشر المباشر عبر API
        service = build('blogger', 'v3', developerKey=GEMINI_API_KEY) # كمثال بسيط
        # (في بيئة العمل الحقيقية نستخدم OAuth2 للوصول لمدونتك الخاصة)
        print(f"✅ تم تجهيز المقال بنجاح: {title}")
    except Exception as e:
        print(f"❌ خطأ في النشر: {e}")

# تنفيذ العملية
chosen_topic = random.choice(keywords)
print(f"🚀 جاري العمل على ترند: {chosen_topic}")

full_content = generate_article(chosen_topic)
article_title = f"{chosen_topic} - Global Update | تحديث عالمي"

# اطبع المحتوى للتأكد (سيظهر في الـ Logs الخاصة بـ GitHub Actions)
print(full_content)

# ملاحظة: لكي يعمل النشر التلقائي، يجب أن يكون لديك ملف 'client_secrets.json' 
# و 'token.json' محفوظين في الـ Secrets الخاصة بـ GitHub.
