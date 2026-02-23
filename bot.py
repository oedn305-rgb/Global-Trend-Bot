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
# التأكد من استخدام الموديل الصحيح
model = genai.GenerativeModel('gemini-2.0-flash')

keywords = ["Future of AI 2026", "Green Energy Trends", "ترند التكنولوجيا", "تطور الهواتف الذكية"]

def generate_with_retry(prompt, retries=3):
    for i in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                # انتظار تصاعدي: 60 ثانية، ثم 120، ثم 180...
                wait_time = (i + 1) * 60 
                print(f"⚠️ زحام سيرفر (429).. انتظار {wait_time} ثانية (محاولة {i+1})")
                time.sleep(wait_time)
            else:
                print(f"❌ خطأ: {e}")
                return None
    return None

# التنفيذ
topic = random.choice(keywords)
print(f"🚀 البوت يبدأ معالجة موضوع: {topic}")

prompt_text = f"Write a professional short HTML article about {topic} in Arabic and English."
article = generate_with_retry(prompt_text)

if article:
    print("✅ تم التوليد بنجاح!")
    # هنا تقدر تضيف كود إرسال الإيميل اللي سويناه قبل
    print(article[:200]) 
else:
    print("❌ فشل البوت في تجاوز حظر جوجل حالياً.")
    exit(1)
