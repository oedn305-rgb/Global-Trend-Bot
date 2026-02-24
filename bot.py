import requests
import smtplib
import time
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 1. إعداداتك (استبدل القيم بين العلامات بدقة)
# ==========================================
API_KEY = "ضـع_مـفتاح_AIza_هـنا"  # تأكد أنه يبدأ بـ AIza ولا توجد مسافات
MY_EMAIL = "your-email@gmail.com"
EMAIL_PASS = "xxxx xxxx xxxx xxxx"  # كلمة سر التطبيقات الـ 16 حرف
BLOGGER_EMAIL = "secret-email@blogger.com"

def generate_article_with_retry(retries=3):
    # رابط الـ API المباشر لتجنب أخطاء المكتبات
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    topics = [
        "أهمية الأمن الرقمي في 2026", 
        "كيف تطور ذكاء الآلة في العام الأخير", 
        "مستقبل الهواتف الذكية"
    ]
    topic = random.choice(topics)
    
    data = {
        "contents": [{"parts": [{"text": f"Write a professional HTML article in Arabic about {topic}. Use H2 and H3 tags, and make it SEO friendly."}]}]
    }

    for i in range(retries):
        try:
            print(f"🚀 محاولة {i+1}: جاري التواصل مع السيرفر...")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            # إذا كان هناك خطأ في المفتاح سيظهر هنا
            if response.status_code != 200:
                print(f"❌ خطأ من السيرفر: {response.status_code} - تأكد من صحة الـ API KEY")
                return None, None
                
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            # تنظيف النص لضمان ظهور HTML فقط
            clean_text = re.sub(r'```html|```', '', text).strip()
            return topic, clean_text
        except Exception as e:
            print(f"⚠️ فشلت المحاولة {i+1}.. السبب: {e}")
            time.sleep(3)
    return None, None

def send_to_blogger(subject, content):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(content, 'html', 'utf-8'))

        print("📧 جاري الإرسال إلى مدونة بلوجر...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return False

# التشغيل الفوري
if __name__ == "__main__":
    subject, article = generate_article_with_retry()
    
    if article:
        if send_to_blogger(subject, article):
            print(f"✨ مبروووك! تم نشر المقال بنجاح: {subject}")
        else:
            print("❌ تم توليد المقال لكن فشل الإرسال للإيميل.")
    else:
        print("❌ فشل البوت في الحصول على المقال. راجع مفتاح الـ API.")
