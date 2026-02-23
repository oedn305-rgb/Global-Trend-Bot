import os
import random
import time
import google.generativeai as genai

# جلب المفاتيح
GEMINI_KEY = os.getenv("GEMINI_KEY")

if not GEMINI_KEY:
    print("❌ GEMINI_KEY is missing!")
    exit(1)

genai.configure(api_key=GEMINI_KEY)

# استخدام موديل 1.5-flash لأنه أكثر استقراراً في الحصص المجانية (Free Tier)
model = genai.GenerativeModel('gemini-1.5-flash')

keywords = ["الطاقة المتجددة 2026", "AI Future", "نيوم والمستقبل"]

def generate_article(topic):
    # تقليل طول الطلب قليلاً لتجنب الـ Quota
    prompt = f"Write a professional short article about {topic}. Dual language: Arabic and English. Use HTML."
    
    # محاولة الطلب مع التعامل مع خطأ الزحام (429)
    for attempt in range(3): # سيحاول 3 مرات
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ زحام في السيرفر، سأنتظر 30 ثانية (محاولة {attempt+1})")
                time.sleep(30)
            else:
                raise e
    return None

try:
    topic = random.choice(keywords)
    print(f"🚀 البدء في معالجة: {topic}")
    
    content = generate_article(topic)
    if content:
        print("✅ تم توليد المقال بنجاح!")
        print(content[:200])
except Exception as e:
    print(f"❌ خطأ نهائي: {e}")
    exit(1)
