import os
import time
import random
import google.generativeai as genai

# جلب المفاتيح
GEMINI_KEY = os.getenv("GEMINI_KEY")
if not GEMINI_KEY:
    print("❌ المفتاح مفقود!")
    exit(1)

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

keywords = ["Future of AI 2026", "Green Energy Trends", "ترند التكنولوجيا"]

def generate_with_retry(prompt, retries=3, delay=45):
    for i in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "delay" in str(e).lower():
                print(f"⚠️ السيرفر طلب انتظار.. سأنتظر {delay} ثانية (محاولة {i+1})")
                time.sleep(delay)
            else:
                print(f"❌ خطأ غير متوقع: {e}")
                return None
    return None

# التنفيذ
topic = random.choice(keywords)
print(f"🚀 معالجة موضوع: {topic}")

article = generate_with_retry(f"Write a short HTML article about {topic} in Arabic and English.")

if article:
    print("✅ تم النجاح!")
    print(article[:200])
else:
    print("❌ فشل التوليد بعد عدة محاولات.")
    exit(1)
