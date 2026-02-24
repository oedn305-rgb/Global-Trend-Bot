import os
import time
import random
import google.generativeai as genai

# جلب المفاتيح
GEMINI_KEY = os.getenv("GEMINI_KEY")
if not GEMINI_KEY:
    print("❌ المفتاح مفقود في GitHub Secrets!")
    exit(1)

genai.configure(api_key=GEMINI_KEY)

# استخدام جمانيا 2.5 فلاش
model_name = 'gemini-2.5-flash' 
model = genai.GenerativeModel(model_name)

keywords = ["Future of AI 2026", "Green Energy Trends", "ترند التكنولوجيا", "تطور الهواتف الذكية"]

def generate_with_retry(prompt, retries=3):
    for i in range(retries):
        try:
            print(f"🔄 محاولة التوليد باستخدام {model_name} (محاولة {i+1})...")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                wait_time = 300 
                print(f"⚠️ زحام سيرفر.. سأنتظر {wait_time/60} دقائق...")
                time.sleep(wait_time)
            else:
                print(f"❌ خطأ تقني: {e}")
                return None
    return None

# التنفيذ
topic = random.choice(keywords)
print(f"🚀 البوت يبدأ معالجة موضوع: {topic}")

# التعديل هنا: طلب مقال مفصل (أكثر من 500 كلمة) لضمان قبول أدسنس
prompt_text = (
    f"Write a very detailed and professional HTML article about {topic}. "
    f"The article should be at least 500 to 700 words long. "
    f"Use Arabic as the primary language and English for technical terms. "
    f"Include an H1 title, several H2 subheadings, bullet points, and a strong conclusion. "
    f"Focus on SEO keywords to attract visitors."
)

article = generate_with_retry(prompt_text)

if article:
    print("✅ نجحت العملية! تم توليد مقال طويل واحترافي.")
    # عرض أول 500 حرف للتأكد
    print("--- بداية المقال ---")
    print(article[:500] + "...") 
else:
    print("❌ فشل التوليد بعد المحاولات.")
    exit(1)
