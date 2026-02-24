import os
import time
import random
import smtplib
import re
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. الإعدادات اليدوية (ضع بياناتك هنا مباشرة)
# --------------------------------------------------
MY_API_KEY = "ضع_هنا_مفتاح_API_الجديد_من_جوجل"
MY_EMAIL = "your-email@gmail.com"
EMAIL_PASS = "xxxx xxxx xxxx xxxx" # كلمة سر التطبيقات الـ 16 حرف
BLOGGER_EMAIL = "secret-email@blogger.com"
# --------------------------------------------------

# إعداد المكتبة
genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # موديل 1.5 حصته أكبر وأكثر استقراراً

def generate_and_send():
    # قائمة مواضيع تقنية احترافية لجذب أدسينس
    keywords = [
        "مستقبل الأمن السيبراني في عام 2026",
        "تأثير الذكاء الاصطناعي على تطوير البرمجيات",
        "كيفية حماية الخصوصية الرقمية في عصر الحوسبة الكمية",
        "أفضل استراتيجيات التسويق بالمحتوى باستخدام AI",
        "تطور الهواتف الذكية وتقنيات الجيل السادس 6G"
    ]
    topic = random.choice(keywords)

    # برومبت (Prompt) احترافي جداً
    prompt = f"""
    اكتب مقالاً طويلاً واحترافياً باللغة العربية حول: {topic}.
    المتطلبات التقنية:
    - استخدم تنسيق HTML بالكامل.
    - استخدم H1 للعنوان و H2 و H3 للعناوين الفرعية.
    - أضف فقرات مرتبة ونقاط توضيحية.
    - اجعل المحتوى مفيداً وتعليمياً (Min 600 words).
    - تجنب الكلمات المتكررة التي توحي بأن النص آلي.
    """

    try:
        print(f"🚀 جاري توليد المقال عن: {topic}...")
        response = model.generate_content(prompt)
        
        # تنظيف النص من علامات المارك داون لضمان تنسيق HTML سليم
        article_content = response.text
        article_content = re.sub(r'```html|```', '', article_content).strip()

        # إعداد الرسالة
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_content, 'html', 'utf-8'))

        # إرسال الإيميل عبر سيرفر جوجل
        print("📧 جاري الإرسال إلى بلوجر...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح: {topic}")

    except Exception as e:
        if "429" in str(e):
            print("⚠️ تجاوزت الحصة اليومية! انتظر قليلاً أو استبدل المفتاح.")
        else:
            print(f"❌ حدث خطأ: {e}")

# تشغيل البوت مرة واحدة
if __name__ == "__main__":
    generate_and_send()
