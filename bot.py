import os
import requests
import smtplib
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run_blogger_bot():
    # جلب الأسرار من إعدادات GitHub
    raw_api_key = os.getenv("GEMINI_KEY")
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    # فحص الأسرار وتنظيف المفتاح
    if not all([raw_api_key, MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("❌ خطأ: بعض الأسرار مفقودة في GitHub Secrets!")
        return
    
    API_KEY = raw_api_key.strip() # تنظيف المفتاح من أي مسافات مخفية

    # استخدام موديل 1.5 Flash لضمان أقصى استقرار مع المفاتيح المجانية
    MODEL_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    topic = random.choice([
        "أهم تقنيات الذكاء الاصطناعي في 2026",
        "مستقبل التدوين الآلي والربح من الإنترنت",
        "كيف تحمي بياناتك الرقمية من الاختراق"
    ])
    
    print(f"📝 جاري محاولة توليد مقال عن: {topic}")

    payload = {
        "contents": [{"parts": [{"text": f"اكتب مقال HTML احترافي بالعربية عن {topic} بتنسيق H2 و H3."}]}]
    }

    try:
        response = requests.post(MODEL_URL, json=payload, timeout=30)
        
        # إذا استمر خطأ 400، سيطبع الكود تفاصيل الخطأ هنا لمساعدتك
        if response.status_code != 200:
            print(f"❌ خطأ من جوجل ({response.status_code}): {response.text}")
            return

        result = response.json()
        article_html = result['candidates'][0]['content']['parts'][0]['text']
        article_html = re.sub(r'```html|```', '', article_html).strip()

        # إرسال الإيميل لبلوجر
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_html, 'html', 'utf-8'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print(f"🏁 تم النشر بنجاح! المقال الآن في مدونتك.")

    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    run_blogger_bot()
