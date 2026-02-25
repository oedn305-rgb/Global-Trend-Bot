import os
import requests
import smtplib
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run_blogger_bot():
    # 1. جلب الأسرار من GitHub (تأكد أن الأسماء تطابق الصورة)
    API_KEY = os.getenv("GEMINI_KEY")
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    # فحص الأمان
    if not all([API_KEY, MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("❌ خطأ: بعض الأسرار مفقودة! تأكد من GEMINI_KEY و MY_EMAIL و EMAIL_PASS و BLOGGER_EMAIL")
        return

    # 2. إعداد الموديل (أحدث إصدار Gemini 2.0 Flash)
    MODEL_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    # قائمة مواضيع "ترند" لعام 2026
    topics = [
        "أهم تقنيات الذكاء الاصطناعي في 2026",
        "كيفية حماية خصوصيتك الرقمية في عصر التطور التقني",
        "مستقبل العمل عن بعد وأدوات الإنتاجية الذكية",
        "تطور الأمن السيبراني لمواجهة التهديدات الحديثة"
    ]
    topic = random.choice(topics)
    print(f"📝 جاري توليد مقال عن: {topic}")

    # 3. طلب توليد المحتوى من جمناي
    payload = {
        "contents": [{
            "parts": [{
                "text": f"اكتب مقال HTML احترافي وطويل باللغة العربية عن {topic}. استخدم تنسيق H2 و H3، واجعله مناسباً لمدونات بلوجر وسهل القراءة."
            }]
        }]
    }

    try:
        response = requests.post(MODEL_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # استخراج النص وتنظيفه
        article_html = result['candidates'][0]['content']['parts'][0]['text']
        article_html = re.sub(r'```html|```', '', article_html).strip()
        print("✅ تم توليد المقال بنجاح.")

        # 4. إرسال المقال إلى بلوجر عبر الإيميل
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_html, 'html', 'utf-8'))

        print(f"📧 جاري الإرسال إلى بلوجر: {BLOGGER_EMAIL}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print(f"🏁 تم النشر بنجاح! مبروك يا مبرمج.")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run_blogger_bot()
