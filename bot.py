import os
import time
import random
import smtplib
import re
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. قائمة المفاتيح (أضف مفاتيحك الجديدة هنا)
API_KEYS = [
    os.getenv("GEMINI_KEY_1"),
    os.getenv("GEMINI_KEY_2") # يفضل استخدام أكثر من مفتاح
]

MY_EMAIL = os.getenv("MY_EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")
BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

def generate_and_send():
    # اختيار مفتاح عشوائي لتوزيع الضغط
    current_key = random.choice(API_KEYS)
    genai.configure(api_key=current_key)
    
    # محاولة استخدام الموديل المطلوب
    model = genai.GenerativeModel('gemini-2.0-flash') 

    keywords = ["أمن المعلومات 2026", "الذكاء الاصطناعي والبرمجة", "مستقبل الطاقة المتجددة"]
    topic = random.choice(keywords)

    prompt = f"اكتب مقال HTML احترافي عن {topic} بالعربية، طويل ومنسق بـ H2 و H3."

    try:
        print(f"🚀 محاولة التوليد باستخدام الموديل 2.0... الموضوع: {topic}")
        response = model.generate_content(prompt)
        article_content = re.sub(r'```html|```', '', response.text).strip()

        # إرسال الإيميل
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_content, 'html', 'utf-8'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print("✅ تم النشر بنجاح!")

    except Exception as e:
        if "429" in str(e):
            print("⚠️ تجاوزت الحصة! السيرفر يطلب الانتظار. سأحاول مرة أخرى بعد دقيقتين...")
            time.sleep(120) # انتظار إجباري
        else:
            print(f"❌ خطأ آخر: {e}")

# تشغيل البوت
generate_and_send()
