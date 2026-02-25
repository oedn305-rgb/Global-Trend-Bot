import os
import requests
import smtplib
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run_secure_bot():
    # --- جلب البيانات من "الأسرار" (Secrets) ---
    # الكود الحين يروح يدور عليهم في ملفات النظام السرية
    API_KEY = os.getenv("API_KEY")
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    # تأكد إن الأسرار موجودة
    if not all([API_KEY, MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("❌ خطأ: لم أجد بعض المفاتيح في ملفات الأسرار! تأكد من إضافتها.")
        return

    # أحدث موديل Gemini 2.0 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    topic = random.choice(["تطور الذكاء الاصطناعي 2026", "حماية البيانات الرقمية", "مستقبل التكنولوجيا"])
    print(f"🚀 جاري توليد المقال باستخدام Gemini 2.0 Flash...")

    payload = {
        "contents": [{"parts": [{"text": f"اكتب مقال HTML احترافي بالعربية عن {topic}."}]}]
    }

    try:
        # 1. طلب المقال
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        article_html = result['candidates'][0]['content']['parts'][0]['text']
        article_html = re.sub(r'```html|```', '', article_html).strip()

        # 2. إعداد وإرسال الإيميل
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_html, 'html', 'utf-8'))

        print(f"📧 جاري الإرسال من {MY_EMAIL} إلى بلوجر...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print("✅ تم النشر بنجاح! المفاتيح ظلت سرية والمقال طار للمدونة.")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run_secure_bot()
