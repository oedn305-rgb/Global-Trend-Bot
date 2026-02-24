import requests
import smtplib
import time
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 1. إعداداتك (تأكد من صحتها 100%)
# ==========================================
API_KEY = "ضـع_مفـتاح_الـ_API_هنا"
MY_EMAIL = "your-email@gmail.com"
EMAIL_PASS = "xxxx xxxx xxxx xxxx"  # كلمة سر التطبيقات
BLOGGER_EMAIL = "secret-email@blogger.com"

def generate_article_with_retry(retries=3):
    """توليد المقال مع محاولة الإعادة في حال فشل السيرفر"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    topics = ["مستقبل التقنية 2026", "أمن المعلومات للجميع", "تطور الذكاء الاصطناعي"]
    topic = random.choice(topics)
    
    data = {
        "contents": [{"parts": [{"text": f"Write a professional HTML article in Arabic about {topic}. Use H2 tags, informative paragraphs, and make it SEO friendly."}]}]
    }

    for i in range(retries):
        try:
            print(f"🚀 محاولة {i+1}: جاري توليد المقال...")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status() # التأكد أن الطلب ناجح (200 OK)
            
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            # تنظيف النص من علامات Markdown
            clean_text = re.sub(r'```html|```', '', text).strip()
            return topic, clean_text
        except Exception as e:
            print(f"⚠️ فشلت المحاولة {i+1}.. السبب: {e}")
            if i < retries - 1:
                time.sleep(5) # انتظر 5 ثواني قبل الإعادة
    return None, None

def send_email(subject, content):
    """إرسال الإيميل بطريقة SSL المستقرة"""
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(content, 'html', 'utf-8'))

        print("📧 جاري الإرسال إلى بلوجر عبر SSL...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return False

# ==========================================
# تشغيل البوت (التنفيذ المضمون)
# ==========================================
if __name__ == "__main__":
    subject, article = generate_article_with_retry()
    
    if article:
        success = send_email(subject, article)
        if success:
            print("✨ مبروك! البوت اشتغل 100% والمقال نُشر.")
        else:
            print("❌ فشل الإرسال رغم توليد المقال.")
    else:
        print("❌ فشل السيرفر في الاستجابة بعد عدة محاولات.")
