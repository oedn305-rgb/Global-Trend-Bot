import os
import random
import google.generativeai as genai
from googleapiclient.discovery import build

# 1. إعدادات الجيمني (استخدام الـ Secrets)
# تأكد أنك سميت السكرت في GitHub بـ GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. إعدادات بلوجر
BLOG_ID = os.getenv("BLOG_ID")

# 3. كلمات البحث
keywords = ["AI news 2026", "Global Trends", "أخبار التقنية", "مستقبل التكنولوجيا"]

def generate_content(topic):
    prompt = (
        f"اكتب مقالاً احترافياً عن {topic} بتنسيق HTML.\n"
        "الجزء الأول: بالعربية (عنوان <h1>، فقرات <h2>).\n"
        "الجزء الثاني: ترجمة إنجليزية كاملة بالأسفل.\n"
        "تأكد من استخدام <div dir='rtl'> للعربي و <div dir='ltr'> للإنجليزي."
    )
    response = model.generate_content(prompt)
    return response.text

# تنفيذ العملية
try:
    topic = random.choice(keywords)
    print(f"Working on: {topic}")
    content = generate_content(topic)
    print("Content generated successfully!")
    # هنا البوت انتهى من توليد النص، تأكد من إعداد OAuth للنشر التلقائي
except Exception as e:
    print(f"Error occurred: {e}")
    exit(1) # هذا يخبر GitHub أن هناك خطأ
