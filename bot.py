import os
import random
import google.generativeai as genai

# جلب المفاتيح من GitHub Secrets
GEMINI_KEY = os.getenv("GEMINI_KEY")
BLOG_ID = os.getenv("BLOG_ID")

if not GEMINI_KEY:
    print("❌ Error: GEMINI_KEY is missing!")
    exit(1)

# إعداد الجيمني باستخدام أحدث موديل 2.0
genai.configure(api_key=GEMINI_KEY)

# استخدام Gemini 2.0 Flash (أسرع وأدق للترجمة)
model = genai.GenerativeModel('gemini-2.0-flash')

keywords = [
    "AI breakthroughs 2026", "Global Economy Trends", 
    "أحدث تقنيات الذكاء الاصطناعي", "مستقبل الطاقة المتجددة",
    "Space Exploration 2026", "أخبار الرياضة العالمية"
]

def generate_article(topic):
    # أمر مخصص لـ Gemini 2.0 لإنشاء محتوى مزدوج اللغة بجودة عالية
    prompt = (
        f"Write a professional, SEO-optimized article about '{topic}'.\n"
        "Instructions:\n"
        "1. Start with an Arabic section (Title <h1>, detailed content with <h2> subheadings) inside <div dir='rtl'>.\n"
        "2. Follow with a full professional English translation below it inside <div dir='ltr'>.\n"
        "3. Use HTML tags for formatting. Include relevant emojis.\n"
        "4. Focus on 2026 trends and future insights."
    )
    
    # محاولة توليد المحتوى
    response = model.generate_content(prompt)
    return response.text

try:
    chosen_topic = random.choice(keywords)
    print(f"🚀 Processing Topic: {chosen_topic} using Gemini 2.0 Flash")
    
    article_content = generate_article(chosen_topic)
    
    # طباعة النتيجة في سجلات GitHub (للتأكد من النجاح)
    print("✅ Content Generated Successfully!")
    print("-" * 30)
    print(article_content[:500] + "...") # طباعة أول 500 حرف للتأكد
    
except Exception as e:
    # في حال استمر الخطأ، سيطبع السبب بدقة
    print(f"❌ Detailed Error: {str(e)}")
    exit(1)
