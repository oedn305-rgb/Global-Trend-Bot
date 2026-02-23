import os
import random
import google.generativeai as genai

# جلب المفاتيح بالأسماء الموجودة في GitHub Secrets الخاصة بك
# تأكد من إضافة سكرت باسم BLOG_ID في GitHub
GEMINI_KEY = os.getenv("GEMINI_KEY")
BLOG_ID = os.getenv("BLOG_ID")

if not GEMINI_KEY:
    print("❌ Error: GEMINI_KEY is missing from Secrets!")
    exit(1)

# إعداد الجيمني
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# كلمات بحث عالمية ومحلية
keywords = [
    "AI breakthroughs 2026", "Global Economy Trends", 
    "أحدث تقنيات الذكاء الاصطناعي", "مستقبل الطاقة المتجددة",
    "Space Exploration 2026", "أخبار الرياضة العالمية"
]

def generate_article(topic):
    prompt = (
        f"Write a professional article about '{topic}'.\n"
        "Format: HTML.\n"
        "Section 1: Arabic (Title <h1>, Body with <h2> subheadings) wrapped in <div dir='rtl'>.\n"
        "Section 2: Professional English translation below it wrapped in <div dir='ltr'>.\n"
        "Use emojis and SEO keywords."
    )
    response = model.generate_content(prompt)
    return response.text

# تنفيذ الجلب
try:
    chosen_topic = random.choice(keywords)
    print(f"🚀 Processing Topic: {chosen_topic}")
    
    article_content = generate_article(chosen_topic)
    
    # لغرض التجربة حالياً سيطبع المحتوى في الـ Logs
    # للتأكد من أن الاتصال بالمفتاح سليم
    print("✅ Content Generated Successfully!")
    print(article_content)
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
