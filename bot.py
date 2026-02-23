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

# تحديث الموديل إلى الإصدار 2.5
# ملاحظة: إذا لم يتفعل الإصدار 2.5 في منطقتك بعد، سيعود الكود تلقائياً لـ 2.0
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
                # انتظار ذكي: بما أنك جربت 60 و 120 وفشلت، سنقفز فوراً لـ 5 دقائق
                wait_time = 300 
                print(f"⚠️ حظر 429 مستمر. سأنتظر {wait_time/60} دقائق لتصفية الـ Quota...")
                time.sleep(wait_time)
            else:
                print(f"❌ خطأ تقني: {e}")
                return None
    return None

# التنفيذ
topic = random.choice(keywords)
print(f"🚀 البوت يبدأ معالجة موضوع: {topic}")

# طلب محتوى مكثف قليلاً للاستفادة من قوة 2.5
prompt_text = f"Write a professional HTML article about {topic} with SEO keywords in Arabic and English."
article = generate_with_retry(prompt_text)

if article:
    print("✅ نجحت العملية باستخدام Gemini 2.5!")
    print(article[:300]) 
else:
    print("❌ حتى Gemini 2.5 واجه ضغطاً كبيراً حالياً.")
    exit(1)
